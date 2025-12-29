from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler
router = APIRouter()

@router.api_route("/api/scan", methods=["GET", "POST", "PUT", "DELETE"])
async def scan_root_proxy(request: Request):
    return await proxy_handler.forward(request, "scan")

@router.api_route("/api/scan/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def scan_path_proxy(request: Request, path: str):
    return await proxy_handler.forward(request, path)