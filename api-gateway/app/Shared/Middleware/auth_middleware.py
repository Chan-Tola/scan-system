from fastapi import Request, Response
from starlette.middleware.base import BaseHTTPMiddleware
# Make sure this path matches where you put session_store.py
from app.Shared.Core.session_store import SESSION_COOKIE_NAME, get_session_data, refresh_session
from app.Shared.Core.config import settings

class AuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # 1. Skip auth for login, logout, docs, and root
        # Note: If your login route is /auth/login, add it here
        if request.url.path in ["/auth/login", "/auth/logout", "/staff/login", "/", "/docs", "/openapi.json"]:
            return await call_next(request)

        # 2. Extract Session ID from Cookie
        session_id = request.cookies.get(SESSION_COOKIE_NAME)
        if not session_id:
            return Response(content="Unauthorized: No Session Cookie", status_code=401)
        
        # 3. Validate in Redis
        user_id = get_session_data(session_id)
        if not user_id:
            return Response(content="Unauthorized: Session Expired", status_code=401)

        # Attach user_id to request state so other routes can see WHO is logged in
        request.state.user_id = user_id
        
        response = await call_next(request)

        # 4. SLIDING LOGIC: Refresh timer on every successful request
        # This keeps the user logged in for another 7 days
        refresh_session(session_id)
        response.set_cookie(
            key=SESSION_COOKIE_NAME,
            value=session_id,
            httponly=True,
            max_age=settings.SESSION_EXPIRY, 
            samesite="lax",
            secure=False # Set to True if using HTTPS
        )
        return response