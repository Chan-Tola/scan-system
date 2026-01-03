# service/api-scan/app/Domain/v1/QR_codes/Schemas/qr_schema.py
from pydantic import BaseModel, Field, ConfigDict, validator
from typing import Optional
from datetime import datetime

# Office info for nested response
class OfficeInfo(BaseModel):
    id: int
    name: str
    public_ip: Optional[str] = None
    model_config = ConfigDict(from_attributes=True)

# Request Schema (for creating QR codes)
class GenerateQRCodeRequest(BaseModel):
    office_id: int = Field(..., description="Office ID to associate with QR code")
    
    @validator('office_id')
    def validate_office_id(cls, v):
        if v <= 0:
            raise ValueError('office_id must be a positive integer')
        return v

# Response Schema (basic - without image)
class QRCodeResponse(BaseModel):
    id: int
    office_id: int
    qr_token: str
    is_active: bool
    office: Optional[OfficeInfo] = None  # Include office details
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Response Schema (with QR code image)
class GenerateQRCodeResponse(BaseModel):
    id: int
    office_id: int
    qr_token: str
    is_active: bool
    qr_code_image: str = Field(..., description="Base64 encoded PNG image")
    office: OfficeInfo = Field(..., description="Office information")  # Include office details
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)

# Update Schema
class UpdateQRCodeRequest(BaseModel):
    is_active: Optional[bool] = None