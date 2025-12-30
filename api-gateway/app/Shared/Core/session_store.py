import redis
import uuid
import json
from app.Shared.Core.config import settings

redis_conn = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    decode_responses=True
)


# The name of the cookie we will send to the browser
SESSION_COOKIE_NAME = 'g_sid'

def create_session(user_id: str, user_data: dict = None) -> str:
    """
    Stores user_id and user_data in Redis with a 7-day timer and returns a unique ID.
    """
    session_id = str(uuid.uuid4())
    
    # Store user data as JSON if provided, otherwise just user_id
    session_data = json.dumps({
        "user_id": user_id,
        "user": user_data
    }) if user_data else user_id

    redis_conn.setex(
        f"session:{session_id}",
        settings.SESSION_EXPIRY,
        session_data
    )
    return session_id

def get_session_data(session_id: str):
    """Returns session data (user_id or full user object)"""
    data = redis_conn.get(f"session:{session_id}")
    if not data:
        return None
    
    # Try to parse as JSON (new format with user data)
    try:
        parsed = json.loads(data)
        return parsed
    except (json.JSONDecodeError, TypeError):
        # Old format: just user_id as string
        return {"user_id": data, "user": None}

def refresh_session(session_id: str):
    """
    SLIDING LOGIC: 
    Resets the expiration timer in Redis back to 7 days.
    """
    redis_conn.expire(f"session:{session_id}", settings.SESSION_EXPIRY)

def delete_session(session_id: str):
    """Removes the session from Redis (Logout)."""
    redis_conn.delete(f"session:{session_id}") 