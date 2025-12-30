from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler_staff
router = APIRouter()

@router.api_route("/api/staff", methods=["GET", "POST", "PUT", "DELETE"])
async def staff_root_proxy(request: Request):
    return await proxy_handler_staff.forward(request, "api/staff")

@router.api_route("/api/staff/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def staff_path_proxy(request: Request, path: str):
    return await proxy_handler_staff.forward(request, f"api/staff/{path}")