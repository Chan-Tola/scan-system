import httpx
from fastapi import APIRouter, Response, HTTPException, status, Request
from app.Shared.Core.session_store import (
    create_session,
    delete_session,
    get_session_data,
    SESSION_COOKIE_NAME
)
from app.Shared.Core.config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login")
async def login(payload: dict, response: Response):
    """
    Gateway Login Bridge:
    - Calls Laravel Octane to verify credentials.
    - If OK, creates Redis session and sets 7-day cookie.
    """
    async with httpx.AsyncClient() as client:
        try:
            # Uses the dynamic property from your config.py
            auth_resp = await client.post(
                settings.public_staff_verify_url,
                json= payload,
                timeout=5.0
            )
        except httpx.RequestError:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                detail="Staff Management Service (Laravel) is offline"
            )
    
    if auth_resp.status_code != 208:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid email or password"
        )
    
    #  Get User Data from Laravel response
    user_data = auth_resp.json()
    user_id = str(user_data.get("id"))

    # Create the Session in Redis (store full user data)
    session_id = create_session(user_id, user_data)

    # Set the Cookie with Sliding Expiration (7 days)
    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,   # Security: JavaScript cannot read this
        max_age=settings.SESSION_EXPIRY,
        samesite="lax",
        secure=False # Set to True in Production (HTTPS)    
    )

    return {
        "status": "success",
        "user": user_data
    }

@router.get("/me")
async def get_current_user(request: Request):
    """
    Get current authenticated user from session.
    - Validates session cookie.
    - Returns user data if session is valid.
    - Returns 401 if session is invalid or expired.
    """
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No session cookie"
        )
    
    # Validate session in Redis and get user data
    session_data = get_session_data(session_id)
    if not session_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired"
        )
    
    # Extract user data from session
    user_data = session_data.get("user")
    if not user_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User data not found in session"
        )
    
    return {
        "status": "success",
        "user": user_data
    }

@router.post("/logout")
async def logout(request: Request, response: Response):
    """
    Standard Logout:
    - Deletes session from Redis.
    - Tells browser to delete the cookie.
    - Works even if already logged out (idempotent).
    """
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    
    # Delete session from Redis if it exists
    if session_id:
        delete_session(session_id)
    
    # Delete cookie from browser (must match the same settings as when it was set)
    response.delete_cookie(
        key=SESSION_COOKIE_NAME,
        httponly=True,      # Must match login cookie settings
        samesite="lax",     # Must match login cookie settings
        secure=False        # Must match login cookie settings
    )
    
    return {
        "status": "success",
        "message": "Logged out successfully"
    }