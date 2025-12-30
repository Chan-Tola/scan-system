import redis
import uuid
from app.Shared.Core.config import settings

redis_conn = redis.Redis(
    host=settings.REDIS_HOST, 
    port=settings.REDIS_PORT, 
    decode_responses=True
)


# The name of the cookie we will send to the browser
SESSION_COOKIE_NAME = 'g_sid'
def create_session(user_id: str) -> str:
    """Stores user_id in Redis with a 7-day timer and returns a unique ID."""
    session_id = str(uuid.uuid4());

    redis_conn.setex(
        f"session:{session_id}",
        settings.SESSION_EXPIRY,
        user_id
    )
    return session_id

def get_session_data(session_id: str):
    return redis_conn.get(f"session:{session_id}")

def refresh_session(session_id: str):
    """
    SLIDING LOGIC: 
    Resets the expiration timer in Redis back to 7 days.
    """
    redis_conn.expire(f"session:{session_id}", settings.SESSION_EXPIRY)

def delete_session(session_id: str):
    """Removes the session from Redis (Logout)."""
    redis_conn.delete(f"session:{session_id}") 