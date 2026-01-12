from fastapi import APIRouter, Depends, status, Request, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import httpx

from app.Shared.Infra.database import get_db
from app.Domain.v1.Attendances.Controllers.attendance_controller import AttendanceService
from app.Domain.v1.Attendances.Schemas.attendance_schema import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
    QRValidationRequest,
    QRValidationResponse,
    PublicIpResponse,
    AttendanceResponse,
    PermissionResponse,
    PermissionRequest
)

router = APIRouter(tags=["Attendance"])

def extract_real_ip(request: Request) -> Optional[str]:
    """
    Extract real client IP from HTTP headers.
    Priority: X-Real-IP → X-Forwarded-For (first public IP) → request.client.host
    
    This function works when accessing through public internet.
    When accessing through local network, it returns Docker/internal IPs.
    """
    # Priority 1: X-Real-IP (set by nginx, most reliable)
    real_ip = request.headers.get("X-Real-IP", "").strip()
    if real_ip:
        # Validate it's a real IP (not Docker/internal)
        if not real_ip.startswith(("172.", "10.", "192.168.", "127.", "localhost")):
            print(f"DEBUG: Extracted public IP from X-Real-IP: {real_ip}")
            return real_ip
        else:
            print(f"DEBUG: X-Real-IP is Docker/internal: {real_ip}")
    
    # Priority 2: X-Forwarded-For (proxy chain)
    forwarded_for = request.headers.get("X-Forwarded-For", "").strip()
    if forwarded_for:
        # Parse comma-separated chain: "ip1, ip2, ip3"
        ip_list = [ip.strip() for ip in forwarded_for.split(",")]
        
        # Find first public IP in chain (leftmost is usually original client)
        for ip in ip_list:
            if ip and not ip.startswith(("172.", "10.", "192.168.", "127.", "localhost")):
                print(f"DEBUG: Extracted public IP from X-Forwarded-For: {ip}")
                return ip
        
        # If no public IP found, use leftmost (original client, even if private)
        if ip_list and ip_list[0]:
            print(f"DEBUG: No public IP in X-Forwarded-For, using leftmost: {ip_list[0]}")
            return ip_list[0]
    
    # Priority 3: Fallback to direct connection IP
    if request.client:
        client_host = request.client.host
        if client_host and client_host != "unknown":
            print(f"DEBUG: Fallback to request.client.host: {client_host}")
            return client_host
    
    print("DEBUG: No IP could be extracted from headers")
    return None

@router.get("/get-public-ip", response_model=PublicIpResponse)
async def get_public_ip():
    """
    Get user's public IP address using external API (ipify.org)
    This endpoint is called by the frontend to get the client's public IP.
    Backend controls the API call for better security and reliability.
    """
    try:
        # Use httpx for async HTTP requests
        async with httpx.AsyncClient(timeout=5.0) as http_client:
            # Primary: Try ipify.org with JSON format
            try:
                response = await http_client.get(
                    "https://api.ipify.org?format=json",
                    headers={"Accept": "application/json"}
                )
                response.raise_for_status()
                data = response.json()
                ip = data.get("ip", "").strip()
                
                if ip:
                    return PublicIpResponse(ip=ip, success=True, message=None)
            except Exception as json_error:
                print(f"DEBUG: Failed to get IP from ipify.org (JSON): {json_error}")
                
                # Fallback: Try ipify.org with text format
                try:
                    response = await http_client.get("https://api.ipify.org", timeout=5.0)
                    response.raise_for_status()
                    ip = response.text.strip()
                    
                    if ip:
                        return PublicIpResponse(ip=ip, success=True, message=None)
                except Exception as text_error:
                    print(f"DEBUG: Failed to get IP from ipify.org (text): {text_error}")
                    raise
    
    except Exception as e:
        print(f"DEBUG: Failed to get public IP: {e}")
        return PublicIpResponse(
            ip=None,
            success=False,
            message="Failed to retrieve public IP address. Please try again later."
        )

@router.post("/validate-qr", response_model=QRValidationResponse)
def validate_qr_code(
    request: QRValidationRequest, 
    http_request: Request,  # Add this to access headers
    db: Session = Depends(get_db)
):
    """Validate QR code before check-in"""
    
    # Priority: Use client-provided IP (from request body) if available
    # Otherwise, extract from server headers (for public internet access)
    if not request.client_ip:
        client_ip = extract_real_ip(http_request)
        if client_ip:
            request.client_ip = client_ip
            print(f"DEBUG: Using server-extracted IP for validation: {client_ip}")
        else:
            print("DEBUG: No IP provided by client and none could be extracted from headers")
    else:
        print(f"DEBUG: Using client-provided IP for validation: {request.client_ip}")
    
    # If still no IP, reject
    if not request.client_ip:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot determine your IP address. Please ensure you are connected to the internet."
        )
    
    return AttendanceService.validate_qr_code(db, request)

@router.post("/check-in", response_model=CheckInResponse, status_code=status.HTTP_201_CREATED)
def check_in(
    request: CheckInRequest, 
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Check in to office using QR code
    
    - Validates QR code
    - Checks for duplicate check-in
    - Calculates if late
    - Creates attendance record
    """
    # Extract user_id from API Gateway header
    # The API Gateway's AuthMiddleware stores user_id in request.state.user_id
    # and should forward it via a custom header
    user_id = http_request.headers.get("X-User-ID")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. X-User-ID header missing."
        )
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
   
    # Priority: Use client-provided IP (from request body) if available
    # Otherwise, extract from server headers (for public internet access)
    if request.client_ip:
        client_ip = request.client_ip
        print(f"DEBUG: Using client-provided IP for check-in: {client_ip}")
    else:
        client_ip = extract_real_ip(http_request)
        if client_ip:
            print(f"DEBUG: Using server-extracted IP for check-in: {client_ip}")
        else:
            print("DEBUG: No IP provided by client and none could be extracted from headers")
    
    # If still no IP, reject
    if not client_ip:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot determine your IP address. Please ensure you are connected to the internet."
        )
    
    # Pass client IP to service for validation
    return AttendanceService.check_in(db, user_id, request, client_ip=client_ip)

# ==================== Check-Out ====================

@router.post("/check-out", response_model=CheckOutResponse, status_code=status.HTTP_200_OK)
def check_out(
    request: CheckOutRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Check out from office
    
    - Updates attendance record with check-out time
    - Calculates work hours
    - Detects early leave (before shift_end)
    - Saves early leave reason if provided
    """
    # Extract user_id from API Gateway header
    user_id = http_request.headers.get("X-User-ID")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. X-User-ID header missing."
        )
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    return AttendanceService.check_out(db, user_id, request)

@router.post("/permission-request", response_model=PermissionResponse, status_code=status.HTTP_201_CREATED)
def submit_permission_request(
    request: PermissionRequest,
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
        Submit Permission request for absence
        _ No IP Validation  required ( can be submitted from anywhere )
        _ Create attendance recoard with status 'absent'
        _ Requires auth ( user_id from header )
    """

    # Extract user_id from API Gateway header
    user_id = http_request.headers.get("X-User-ID")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. X-User-ID header missing."
        )

    try: 
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    # Call service to create permission request
    return AttendanceService.create_permission_request(db, user_id, request)

#  Get Attendance  For Staff after Login
@router.get("/today-attendance", response_model=AttendanceResponse, status_code=status.HTTP_200_OK)
def get_today_attendance(
    http_request: Request,
    db: Session = Depends(get_db)
):
    """
    Get today's attendance record for the authenticated user
    
    - Returns attendance if exists
    - Returns 404 if no attendance found for today
    - Used to check if user is checked in (for showing check-out button)
    """
    # Extract user_id from API Gateway header
    user_id = http_request.headers.get("X-User-ID")
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not authenticated. X-User-ID header missing."
        )
    
    try:
        user_id = int(user_id)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid user ID format"
        )
    
    return AttendanceService.get_today_attendance(db, user_id)
