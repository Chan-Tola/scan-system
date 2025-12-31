from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# 1. Import the routers from your new DDD paths
from app.Domain.v1.Auth.route_auth import router as auth_router
from app.Domain.v1.Scan.route_scan import router as scan_router
from app.Domain.v1.Staff.route_staff import router as staff_router
from app.Domain.v1.Offices.route_office import router as office_router
from app.Shared.Infra.reverse_proxy import proxy_handler, proxy_handler_staff
from app.Shared.Middleware.auth_middleware import AuthMiddleware

app = FastAPI(title="API Gateway (DDD)")

# 1. CORS middleware (must be added before other middleware)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",  # Vite dev server
        "http://localhost:3000",  # Alternative dev port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,  # Required for cookies
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

# 2. Auth middleware
app.add_middleware(AuthMiddleware)

# 3. Include the routers correctly
app.include_router(auth_router) # Handles /auth/login
app.include_router(scan_router) # Handles /scan
app.include_router(staff_router) # Handles /
app.include_router(office_router) # Handles /api/offices

@app.get("/")
async def health_check():
    return {"status": "Gateway is Healthy", "version": "v1-ddd"}

@app.on_event("shutdown")
async def shutdown_event():
    await proxy_handler.close()
    await proxy_handler_staff.close()