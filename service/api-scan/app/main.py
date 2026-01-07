# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.Shared.Infra.database import get_db  # ✅ Fixed
from app.Domain.v1.Offices.Routes.route_office import router as office_router
from app.Domain.v1.QR_codes.Routes.route_qr import router as qr_router

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
app.include_router(office_router,prefix="/offices")
app.include_router(qr_router,prefix="/generate-code")