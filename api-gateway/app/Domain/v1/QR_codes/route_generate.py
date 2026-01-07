from fastapi import APIRouter, Request
from app.Shared.Infra.reverse_proxy import proxy_handler

router = APIRouter()

@router.api_route("", methods=["GET", "POST", "PUT", "DELETE"])
async def generate_code(request: Request):
    """Generate a new QR code"""
    return await proxy_handler.forward(request,"generate-code")

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def generate_code_path_proxy(request: Request, path: str):
    """Proxy requests with sub-paths to the generate-code endpoint in API_SCAN_URL service"""
    return await proxy_handler.forward(request, f"generate-code/{path}")