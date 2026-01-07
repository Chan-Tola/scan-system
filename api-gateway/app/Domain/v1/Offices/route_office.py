from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler
router = APIRouter()

@router.api_route("", methods=["GET", "POST", "PUT", "DELETE"])
async def office_root_proxy(request: Request):
    return await proxy_handler.forward(request, "offices")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def office_path_proxy(request: Request, path: str):
    return await proxy_handler.forward(request, f"offices/{path}")