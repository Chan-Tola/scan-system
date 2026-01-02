from fastapi import APIRouter, Depends, status, Response
from sqlalchemy.orm import Session
from typing import List, Optional
from app.Shared.Infra.database import get_db
from app.Domain.v1.QR_codes.Controllers.qr_controller import QRCodeService
from app.Domain.v1.QR_codes.Schemas.qr_schema import (
    GenerateQRCodeRequest,
    QRCodeResponse,
    GenerateQRCodeResponse
)

router = APIRouter(prefix="/generate-code", tags=["QR Code Generation"])

# Create a new QR code for a new office
@router.post("", response_model=GenerateQRCodeResponse, status_code=status.HTTP_201_CREATED)
def create_qr(request: GenerateQRCodeRequest, db: Session = Depends(get_db)):
    return QRCodeService.generate_qr_code(db, request)

# Regenerate the QR token for an existing QR code
@router.post("/{qr_code_id}/regenerate", response_model=GenerateQRCodeResponse)
def refresh_qr(qr_code_id: int, db: Session = Depends(get_db)):
    """Type B: Update existing record with a brand new token/image"""
    return QRCodeService.regenerate_qr_token(db, qr_code_id)

# Get all QR codes
@router.get("", response_model=List[QRCodeResponse])
def list_qr(
    skip: int = 0, limit: int = 100, 
    is_active: Optional[bool] = None, 
    office_id: Optional[int] = None, 
    db: Session = Depends(get_db)
):
    return QRCodeService.get_all_qr_codes(db, skip, limit, is_active, office_id)

# Get a QR code by ID
@router.get("/{qr_code_id}", response_model=QRCodeResponse)
def get_qr_by_id(qr_code_id: int, db: Session = Depends(get_db)):
    """Get QR code by ID"""
    return QRCodeService.get_qr_code_by_id(db, qr_code_id)

# Get a QR code by token
@router.get("/token/{qr_token}", response_model=QRCodeResponse)
def get_qr_by_token(qr_token: str, db: Session = Depends(get_db)):
    """Get QR code by token"""
    return QRCodeService.get_qr_code_by_token(db, qr_token)

# Get a QR code image by ID
@router.get("/{qr_code_id}/image")
def get_qr_image(qr_code_id: int, db: Session = Depends(get_db)):
    """Get QR code image by ID"""
    image_data = QRCodeService.get_qr_code_image(db, qr_code_id)
    return {"qr_code_image": image_data}

# Delete a QR code
@router.delete("/{qr_code_id}", status_code=status.HTTP_204_NO_CONTENT)
def remove_qr(qr_code_id: int, db: Session = Depends(get_db)):
    QRCodeService.delete_qr_code(db, qr_code_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)