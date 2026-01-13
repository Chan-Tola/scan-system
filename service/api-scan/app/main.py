# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.Shared.Infra.database import get_db  # ✅ Fixed
from app.Domain.v1.Offices.Routes.route_office import router as office_router
from app.Domain.v1.QR_codes.Routes.route_qr import router as qr_router
from app.Domain.v1.Attendances.Routes.route_attendance import router as attendance_router
from app.Domain.v1.Dashboard.Routes.route_dashboard import router as dashboard_router  # ✅ Added
# Import models so SQLAlchemy registers them in metadata for foreign key resolution
from app.Domain.v1.Users.Models.user_model import User
from app.Domain.v1.Attendances.Models.attendance_reason_model import AttendanceReason

app = FastAPI(
    title="API Scan Service",
    description="Backend service for QR Management and Scanning",
    version="1.0.0"
)

# Root Endpoint
@app.get("/")
async def root():
    return {"service": "API Scan Service", "status": "active"}

@app.get("/health", tags=["System"])
async def health_check():
    return {"status": "healthy"}

# Include routers
app.include_router(office_router, prefix="/offices")
app.include_router(qr_router, prefix="/generate-code")
app.include_router(attendance_router, prefix="/scan")
app.include_router(dashboard_router, prefix="/scan")  # ✅ Added - dashboard under /scan prefix
