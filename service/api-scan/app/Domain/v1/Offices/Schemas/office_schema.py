from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class OfficeBase(BaseModel):
    name: str
    public_ip: Optional[str] = None  # Changed to Optional to match database

class OfficeCreate(OfficeBase):
    pass

class OfficeUpdate(BaseModel):
    name: Optional[str] = None
    public_ip: Optional[str] = None

class OfficeResponse(OfficeBase):
    id: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)