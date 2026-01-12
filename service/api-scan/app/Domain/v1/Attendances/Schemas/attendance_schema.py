from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime, date, time

# Public IP Response
class PublicIpResponse(BaseModel):
    ip: Optional[str] = None
    success: bool
    message: Optional[str] = None

# Office info for nested response
class OfficeInfo(BaseModel):
    id:int
    name:str
    public_ip: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# User info for nested response 
class UserInfo(BaseModel):
    id:int
    username:str
    email:str
    model_config = ConfigDict(from_attributes=True)

# Attendance Response Schemas
class AttendanceResponse(BaseModel):
    id: int
    user_id: int
    office_id: Optional[int] = None
    log_date: date
    check_in: Optional[time] = None
    check_out: Optional[time] = None
    status: str  # present, late, absent
    minutes_late: int
    work_hours: Optional[float] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    # Nested relationships
    office: Optional[OfficeInfo] = None
    attendance_reasons: Optional[list["AttendanceReasonResponse"]] = []
    
    model_config = ConfigDict(from_attributes=True)


# Attendance Reason Response
class AttendanceReasonResponse(BaseModel):
    id: int
    attendance_id: int
    reason_type: str  # late, early_leave
    reason: str
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# QR Validate Request Schemas
class QRValidationRequest(BaseModel):
    qr_token: str = Field(..., description="QR code token to validate")
    client_ip: Optional[str] = Field(None, description="Client IP Address (can be extracted from request)")

    @validator('qr_token')
    def validate_qr_token(cls, v):
        if not v or len(v.strip()) == 0:
            raise ValueError('qr_token is required')
        return v.strip()

# QR Validation Response
class QRValidationResponse(BaseModel):
    valid: bool
    message: str
    office: Optional[OfficeInfo] = None


# Check-In Request
class CheckInRequest(BaseModel):
    qr_token: str = Field(..., description="QR code token for check in")
    client_ip: Optional[str] = Field(None, description="Client IP Address (can be provided by client)")
    @validator('qr_token')
    def validate_qr_token(cls, v):
        if not v or len(v.strip())== 0:
            raise ValueError('qr_token is required')
        return v.strip()

# Check In Response
class CheckInResponse(BaseModel):
    message: str
    attendance: AttendanceResponse
    is_late: bool
    minutes_late: int

# Check-Out Request
class CheckOutRequest(BaseModel):
    qr_token: Optional[str] = Field(None, description="QR code token (optional)")
    reason_type: Optional[str] = Field(None, description="Reason type: early_leave")
    reason: Optional[str] = Field(None, description="Reason for early leave")

# Check-Out Response
class CheckOutResponse(BaseModel):
    message: str
    attendance: AttendanceResponse
    work_hours: float
    is_early_leave: bool

# Permission Request (for absence)
class PermissionRequest(BaseModel):
    date: str = Field(..., description="Date of absence (YYYY-MM-DD format)")
    reason_type: str = Field(..., description="Type: absent")
    reason: str = Field(..., min_length=10, max_length=500, description="Detailed reason for absence")
    
    @validator('date')
    def validate_date(cls, v):
        # Parse string date to date object
        try:
            parsed_date = datetime.strptime(v, '%Y-%m-%d').date()
        except ValueError:
            raise ValueError('Date must be in YYYY-MM-DD format')
        
        # Date must be today or future
        if parsed_date < date.today():
            raise ValueError('Date cannot be in the past')
        
        return v  # Return original string format
    
    @validator('reason_type')
    def validate_reason_type(cls, v):
        # Only accept 'absent' from frontend
        if v != 'absent':
            raise ValueError('reason_type must be "absent"')
        return v
    
    @validator('reason')
    def validate_reason(cls, v):
        if not v or len(v.strip()) < 10:
            raise ValueError('Reason must be at least 10 characters')
        return v.strip()

# Permission Response
class PermissionResponse(BaseModel):
    message: str
    attendance: AttendanceResponse
    attendance_reason: AttendanceReasonResponse
