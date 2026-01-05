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
    - Calls Laravel to verify credentials.
    - If OK, catches the full profile immediately and stores in Redis.
    - Achieves high performance by serving profile from cache later.
    """
    async with httpx.AsyncClient() as client:
        try:
            # 1. Verify Credentials
            auth_resp = await client.post(
                settings.public_staff_verify_url,
                json=payload,
                timeout=5.0
            )
            
            if auth_resp.status_code != 208:
                raise HTTPException(status_code=401, detail="Invalid email or password")
            
            basic_user = auth_resp.json()
            user_id = str(basic_user.get("id"))

            # 2. Fetch Full Profile immediately (One-time cost at login)
            profile_resp = await client.post(
                settings.public_staff_me_url,
                json={"user_id": user_id},
                timeout=5.0
            )
            
            user_data = basic_user
            if profile_resp.status_code == 200:
                user_data = profile_resp.json()

        except httpx.RequestError:
            raise HTTPException(status_code=503, detail="Staff service offline")

    # 3. Store EVERYTHING in Redis (User + Profile)
    session_id = create_session(user_id, user_data)

    response.set_cookie(
        key=SESSION_COOKIE_NAME,
        value=session_id,
        httponly=True,
        max_age=settings.SESSION_EXPIRY,
        samesite="lax",
        secure=False
    )

    return {
        "status": "success",
        "user": user_data
    }

@router.get("/me")
async def get_current_user(request: Request):
    """
    Ultra-Fast Me Endpoint:
    - Zero external HTTP calls.
    - Reads directly from local Redis session.
    """
    session_id = request.cookies.get(SESSION_COOKIE_NAME)
    if not session_id:
        raise HTTPException(status_code=401, detail="No session")
    
    session_data = get_session_data(session_id)
    if not session_data:
        raise HTTPException(status_code=401, detail="Session expired")
    
    # Session data found? Return immediately (Blazing fast!)
    return {
        "status": "success",
        "user": session_data.get("user")
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