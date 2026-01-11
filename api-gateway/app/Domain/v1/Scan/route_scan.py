from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler

router = APIRouter()

@router.api_route("", methods=["GET", "POST", "PUT", "DELETE"])
async def scan_root_proxy(request: Request):
    return await proxy_handler.forward(request, "scan")
    
# Catch-all route for other scan endpoints
@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def scan_path_proxy(request: Request, path: str):
    """Proxy all other scan requests to the api-scan service"""
    return await proxy_handler.forward(request, f"scan/{path}")
