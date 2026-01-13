from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler_staff

router = APIRouter()

@router.get("/")
async def get_history(request: Request):
    """Get paginated attendance history with filters"""
    return await proxy_handler_staff.forward(request, "api/attendance-records")

@router.get("/statistics")
async def get_statistics(request: Request):
    """Get monthly statistics"""
    return await proxy_handler_staff.forward(request, "api/attendance-records/statistics")

@router.get("/export")
async def export_history(request: Request):
    """Export attendance history to Excel"""
    return await proxy_handler_staff.forward(request, "api/attendance-records/export")
    