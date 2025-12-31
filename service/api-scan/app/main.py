# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Optional
from app.Shared.Infra.database import get_db  # ✅ Fixed
from app.Domain.v1.Offices.Routes.route_office import router as office_router

app = FastAPI(title="API Scan Service")

# Include routers
app.include_router(office_router)

@app.get("/")
async def root():
    return {
        "service": "API Scan Service",
        "status": "running",
        "version": "v1"
    }

@app.get("/health")  # ✅ Fixed: removed colon
async def health_check(db: Session = Depends(get_db)):  # ✅ Fixed: added db parameter
    """Health check endpoint"""
    try:
        from sqlalchemy import text
        result = db.execute(text("SELECT 1")).scalar()
        return {
            "status": "healthy",
            "database": "connected" if result == 1 else "error",
            "service": "api-scan"
        }
    except Exception as e:
        return {
            "status": "unhealthy",
            "database": f"error: {str(e)}",
            "service": "api-scan"
        }

@app.get("/scan")
def scan_code(code: Optional[str] = None, db: Session = Depends(get_db)):
    """Example scan endpoint"""
    from sqlalchemy import text
    result = db.execute(text("SELECT 1")).scalar()
    
    if code is None:
        return {
            "message": "Scan endpoint is ready. Provide a 'code' query parameter.",
            "db_connection": "ok" if result == 1 else "error"
        }
    
    return {
        "scanned_code": code,
        "timestamp": "2025-12-29",
        "db_connection": "ok" if result == 1 else "error"
    }