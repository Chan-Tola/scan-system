import structlog
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from contextlib import asynccontextmanager

# Import configuration and shared utilities
from app.Shared.Middleware.auth_middleware import AuthMiddleware
from app.Shared.Infra.reverse_proxy import proxy_handler, proxy_handler_staff
from app.Shared.Core.limiter import limiter
from app.Shared.Core.config import settings

# Import routers
from app.Domain.v1.Auth.route_auth import router as auth_router
from app.Domain.v1.Scan.route_scan import router as scan_router
from app.Domain.v1.Staff.route_staff import router as staff_router
from app.Domain.v1.Offices.route_office import router as office_router
from app.Domain.v1.QR_codes.route_generate import router as generate_router
from app.Domain.v1.Attendance_Records.route_attendance_record import router as attendance_record_router

# Prepare Logger for Error
logger = structlog.get_logger()

# Lifespan for management Shutdown Gatway (Claen Shutdown)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Sartup
    logger.info("gateway_startup", status="running")
    yield
    # Shutdown: close the HTTP Clients for protect Memory Leak
    await proxy_handler.close()
    await proxy_handler_staff.close()
    logger.info("gateway_shutdown", status="stopped")

# Create Limiter that use the redis connection that import from the session_store
# I use storage_uri for connect to Redis database , Rate Limit

app = FastAPI(
    title="API Gateway (DDD)",
    lifespan=lifespan
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS Middlewares
if settings.CORS_ORIGINS:
    allow_origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")]
else:
    # Development fallback
    allow_origins = [
        "http://localhost:5173",
        "http://192.168.18.119:5173",
        "https://192.168.18.119:5173",
    ]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allow_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# Auth middleware
app.add_middleware(AuthMiddleware)

#  Include the routers correctly
app.include_router(
    auth_router,
    prefix="/api/auth", 
    tags=["Authentication"]
)
app.include_router(
    scan_router,
    prefix="/api/scan", 
    tags=["Scan Management"]
) 
app.include_router(
    staff_router,
    prefix="/api/staff", 
    tags=["Staff Management"]
)

app.include_router(
    office_router,
    prefix="/api/offices",
    tags=["Office Management"]
) 

app.include_router(
    generate_router,
    prefix="/api/generate-code", 
    tags=["Code Generate"]
)

app.include_router(
    attendance_record_router,
    prefix="/api/attendance-records",
    tags=["History Management"]
)

# Root Health Check (សម្រាប់ Docker/Kubernetes)
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "api-gateway"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
