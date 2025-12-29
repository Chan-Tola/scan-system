import httpx
from fastapi import Request, Response
from app.Shared.Core.config import settings

class ReverseProxy:
    def __init__(self,base_url: str):
        self.client = httpx.AsyncClient(base_url=base_url, timeout=30.0)

    async def forward(self, request: Request, path: str):
        target_url = f"/{path}" if path else "/"

        # forward query parameters
        query_params = dict(request.query_params)
        body = await request.body() if request.method in ["POST", "PUT", "PATCH"] else None

        # Forward headers (cleaning technical ones)
        headers = dict(request.headers)
        headers.pop("host", None)
        headers.pop("connection", None)

        try:
            response = await self.client.request(
                method= request.method,
                url= target_url,
                params = query_params,
                content = body,
                headers = headers,
                follow_redirects=True
            )
            return Response(
                content= response.content,
                status_code= response.status_code,
                headers= dict(response.headers),
                media_type= response.headers.get("content-type")
            )
        except httpx.RequestError as e:
            return Response(content=f"Service Unavailable: {str(e)}", status_code=503)
    async def close(self):
        await self.client.aclose()

# Create a single instance to be used everywhere
# proxy_handler = ReverseProxy()
# Create two handlers
proxy_handler = ReverseProxy(settings.API_SCAN_URL);
proxy_handler_staff = ReverseProxy(settings.API_STAFF_URL);