import httpx
from fastapi import Request, Response
from fastapi.responses import StreamingResponse
from app.Shared.Core.config import settings

class ReverseProxy:
    def __init__(self, base_url: str):
        # Increase timeout to 120s for large image uploads to Cloudinary
        # Add connection limits to prevent resource exhaustion
        self.client = httpx.AsyncClient(
            base_url=base_url,
            timeout=120.0,
            limits=httpx.Limits(max_connections=100, max_keepalive_connections=20),
            http2=True
        )

        # Security: Maximum request/response size (100MB)
        self.max_request_size = 100 * 1024 * 1024  # 100MB
        self.max_response_size = 100 * 1024 * 1024  # 100MB

    def _clean_headers(self, headers: dict, request: Request) -> dict:
        """Clean and secure headers before forwarding"""
        cleaned = dict(headers)
        
        # Remove headers that shouldn't be forwarded
        headers_to_remove = [
            "host", "connection", "content-length",  # Technical headers
            "x-forwarded-host", "x-forwarded-proto",  # Already set below
            # "authorization", "cookie",  # Security: Don't forward auth headers (if needed)
            "x-real-ip", "x-forwarded-for",  # Will be set correctly below
        ]
        for header in headers_to_remove:
            cleaned.pop(header, None)
        
        # IMPORTANT: Keep cookie header - Laravel Sanctum needs it for authentication
        # The cookie header contains the session cookie that Sanctum uses
        
        # ENHANCED: Get real client IP (handles Docker, proxies, etc.)
        def get_client_ip(request: Request) -> str:
            """
            Extract the real client IP address, even behind Docker/proxies.
            Priority:
            1. Parse X-Forwarded-For chain and find first public IP
            2. X-Real-IP header (if public)
            3. request.client.host (fallback)
            
            Returns the first public IP found, or the last IP in chain if no public IP exists.
            """
            # Parse X-Forwarded-For chain (format: "client_ip, proxy1_ip, proxy2_ip, ...")
            # The leftmost IP is the original client, rightmost is the last proxy
            forwarded_for = request.headers.get("x-forwarded-for", "")
            if forwarded_for:
                # Split by comma and process each IP (left to right = client to proxies)
                ip_list = [ip.strip() for ip in forwarded_for.split(",")]
                
                # Strategy: Find the FIRST public IP in the chain
                # This is typically the client's real public IP (NAT gateway IP)
                for ip in ip_list:
                    # Skip empty or invalid IPs
                    if not ip or ip == "unknown":
                        continue
                    # Skip Docker/internal/private IPs
                    if not ip.startswith(("172.", "10.", "192.168.", "127.", "localhost")):
                        print(f"🔍 Found public IP in X-Forwarded-For chain: {ip}")
                        return ip
                
                # If no public IP found, use the leftmost (original client) IP
                # This handles cases where client is on local network
                if ip_list and ip_list[0]:
                    print(f"🔍 No public IP in chain, using leftmost IP: {ip_list[0]}")
                    return ip_list[0]
            
            # Check X-Real-IP header (set by nginx)
            real_ip = request.headers.get("x-real-ip", "")
            if real_ip and real_ip != "unknown":
                # Prefer public IPs, but accept private IPs as fallback
                if not real_ip.startswith(("172.", "10.", "192.168.", "127.", "localhost")):
                    print(f"🔍 Found public IP in X-Real-IP: {real_ip}")
                    return real_ip
                else:
                    print(f"🔍 X-Real-IP is private: {real_ip}")
                    return real_ip
            
            # Fallback to direct connection IP
            client_host = request.client.host if request.client else "unknown"
            print(f"🔍 Fallback to request.client.host: {client_host}")
            
            return client_host
                
        client_ip = get_client_ip(request)
        
        # DEBUG: Log the captured IP address
        print(f"🔍 Captured Client IP: {client_ip}")
        print(f"   Request from: {request.client.host if request.client else 'unknown'}")
        print(f"   X-Forwarded-For: {request.headers.get('x-forwarded-for', 'not set')}")
        
        # Security: Add proper forwarding headers
        cleaned["X-Real-IP"] = client_ip
        cleaned["X-Forwarded-For"] = client_ip  # Send real public IP to backend
        cleaned["X-Forwarded-Proto"] = request.url.scheme # tell backend if user from http or https
        cleaned["X-Forwarded-Host"] = request.headers.get("host", "unknown") # tell backend where user come from domain
        
        # IMPORTANT: Forward authenticated user_id to backend services
        # The AuthMiddleware stores user_id in request.state.user_id
        if hasattr(request.state, "user_id"):
            cleaned["X-User-ID"] = str(request.state.user_id)
        
        return cleaned


    def _validate_path(self, path: str) -> bool:
        """Security: Validate path to prevent path traversal attacks"""
        # set path for the route so the user can not go to another route that I set
        # Prevent path traversal (../, ..\, etc.) 
        if ".." in path or path.startswith("/"):
            # Allow / at start but check for traversal
            if ".." in path:
                return False
        # Prevent absolute paths
        if path.startswith("//") or "://" in path:
            return False
        return True

    async def forward(self, request: Request, path: str):
        # Security: Validate path
        if not self._validate_path(path):
            return Response(
                content='{"error": "Invalid path"}',
                status_code=400,
                media_type="application/json"
            )

        target_url = f"/{path}" if path else "/"

        # Check if this is a multipart request (for image uploads)
        content_type = request.headers.get("content-type", "").lower()
        is_multipart = "multipart/form-data" in content_type and request.method in ["POST", "PUT", "PATCH"]
  
        # Security: Clean headers
        headers = self._clean_headers(dict(request.headers), request)

                # IMPORTANT: tell Laravel this is an API request
        if "accept" not in headers or not headers.get("accept"):
            headers["Accept"] = "application/json"

        try:
            # PATH 1: Multipart/Form-Data (Streaming for large image uploads)
            if is_multipart:
                async def request_generator():
                    total_size = 0
                    async for chunk in request.stream():
                        total_size += len(chunk)
                        # Security: Enforce size limit
                        if total_size > self.max_request_size:
                            raise ValueError(f"Request body exceeds maximum size of {self.max_request_size} bytes")
                        yield chunk

                async with self.client.stream(
                    method=request.method,
                    url=target_url,
                    params=dict(request.query_params),
                    content=request_generator(),
                    headers=headers,
                    follow_redirects=True
                ) as response:
                    # Security: Clean response headers (remove sensitive info)
                    resp_headers = dict(response.headers)
                    resp_headers.pop("server", None)  # Don't expose backend server info
                    resp_headers.pop("x-powered-by", None)  # Don't expose backend tech stack
                    
                    # SMART HANDLING: Check if response is JSON or binary
                    # JSON responses (like success/error messages) should be buffered for proper frontend handling
                    # Binary responses (like images) should be streamed for performance
                    response_content_type = response.headers.get("content-type", "").lower()
                    is_json_response = "application/json" in response_content_type
                    
                    if is_json_response:
                        # BUFFER JSON responses for proper error handling in frontend
                        content = await response.aread()
                        if len(content) > self.max_response_size:
                            return Response(
                                content='{"error": "Response too large"}',
                                status_code=413,
                                media_type="application/json"
                            )
                        
                        return Response(
                            content=content,
                            status_code=response.status_code,
                            headers=resp_headers,
                            media_type=response_content_type
                        )
                    else:
                        # STREAM binary responses (images, files) for performance
                        async def response_generator():
                            total_size = 0
                            async for chunk in response.aiter_bytes():
                                total_size += len(chunk)
                                # Security: Enforce size limit
                                if total_size > self.max_response_size:
                                    raise ValueError("Response too large")
                                yield chunk
                        
                        return StreamingResponse(
                            response_generator(),
                            status_code=response.status_code,
                            headers=resp_headers,
                            media_type=response_content_type
                        )

            # PATH 2: Standard Requests (GET, JSON POST, etc.) - Simple pass-through
            else:
                # forward query parameters
                query_params = dict(request.query_params)
                
                # Security: Validate request body size before reading
                if request.method in ["POST", "PUT", "PATCH"]:
                    content_length = request.headers.get("content-length")
                    if content_length and int(content_length) > self.max_request_size:
                        return Response(
                            content='{"error": "Request body too large"}',
                            status_code=413,
                            media_type="application/json"
                        )
                    body = await request.body()
                    if len(body) > self.max_request_size:
                        return Response(
                            content='{"error": "Request body too large"}',
                            status_code=413,
                            media_type="application/json"
                        )
                else:
                    body = None

                response = await self.client.request(
                    method=request.method,
                    url=target_url,
                    params=query_params,
                    content=body,
                    headers=headers,
                    follow_redirects=True
                )
                
                # Security: Check response size
                if len(response.content) > self.max_response_size:
                    return Response(
                        content='{"error": "Response too large"}',
                        status_code=413,
                        media_type="application/json"
                    )
                
                # Security: Clean response headers
                resp_headers = dict(response.headers)
                resp_headers.pop("server", None)  # Don't expose backend server info
                resp_headers.pop("x-powered-by", None)  # Don't expose backend tech stack
                
                return Response(
                    content=response.content,
                    status_code=response.status_code,
                    headers=resp_headers,
                    media_type=response.headers.get("content-type")
                )

        except ValueError as e:
            # Security: Don't expose internal error details
            return Response(
                content='{"error": "Invalid request"}',
                status_code=400,
                media_type="application/json"
            )
        except httpx.TimeoutException:
            # Security: Generic timeout error
            return Response(
                content='{"error": "Request timeout"}',
                status_code=504,
                media_type="application/json"
            )
        except httpx.RequestError as e:
            # Security: Don't expose internal error details
            return Response(
                content='{"error": "Service unavailable"}',
                status_code=503,
                media_type="application/json"
            )
        except Exception as e:
            # Security: Catch-all to prevent info leakage
            return Response(
                content='{"error": "Internal server error"}',
                status_code=500,
                media_type="application/json"
            )

    async def close(self):
        await self.client.aclose()

# Create two handlers
proxy_handler = ReverseProxy(settings.API_SCAN_URL)
proxy_handler_staff = ReverseProxy(settings.API_STAFF_URL)