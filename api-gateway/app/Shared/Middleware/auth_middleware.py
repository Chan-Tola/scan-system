from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
from app.Shared.Core.session_store import SESSION_COOKIE_NAME, get_session_data, refresh_session
from app.Shared.Core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. SECURITY: Allow OPTIONS requests to pass through (CORS preflight)
        # OPTIONS requests are metadata-only and don't access data, so no auth needed
        # The CORS middleware will handle adding proper CORS headers
        if request.method == "OPTIONS":
            return await call_next(request)
        
        # 2. Skip auth for public endpoints (login, logout, me, docs, and root)
        # Note: /auth/me validates its own session
        public_paths = ["/auth/login", "/auth/logout", "/auth/me", "/staff/login", "/", "/docs", "/openapi.json"]
        if request.url.path in public_paths:
            return await call_next(request)

        # 3. SECURITY: Extract and validate Session ID from Cookie
        session_id = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_id:
            return self._unauthorized_response(request, "Unauthorized: No Session Cookie")
        
        # 4. SECURITY: Validate session in Redis
        session_data = get_session_data(session_id)
        if not session_data:
            return self._unauthorized_response(request, "Unauthorized: Session Expired")

        # 5. SECURITY: Extract and validate user_id
        user_id = session_data if isinstance(session_data, str) else session_data.get("user_id")
        if not user_id:
            return self._unauthorized_response(request, "Unauthorized: Invalid Session")

        # 6. SECURITY: Attach user_id to request state for downstream use
        request.state.user_id = user_id
        
        # Process the authenticated request
        response = await call_next(request)

        # 7. SECURITY: Sliding session expiration - refresh on every request
        refresh_session(session_id)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,  # SECURITY: Prevent XSS attacks
            max_age=settings.SESSION_EXPIRY,
            samesite="lax",  # SECURITY: Prevent CSRF attacks
            secure=False  # Set to True in production (HTTPS required)
        )
        return response
    
    def _unauthorized_response(self, request: Request, message: str) -> Response:
        """
        Create 401 response with CORS headers for browser compatibility.
        This ensures error responses include CORS headers so browsers can read the error.
        """
        response = Response(content=message, status_code=401)
        
        # Get origin from request and validate against allowed origins
        origin = request.headers.get("origin")
        allowed_origins = [
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ]
        
        # Only add CORS headers if origin is in allowed list (security)
        if origin in allowed_origins:
            response.headers["Access-Control-Allow-Origin"] = origin
            response.headers["Access-Control-Allow-Credentials"] = "true"
            response.headers["Access-Control-Allow-Methods"] = "GET, POST, PUT, DELETE, OPTIONS"
            response.headers["Access-Control-Allow-Headers"] = "*"
        
        return response