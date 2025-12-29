from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler_staff

router = APIRouter()

@router.api_route("/api/staff/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def staff_proxy(request: Request, path: str):
    return await proxy_handler_staff.forward(request, path)