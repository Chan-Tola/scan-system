from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime, timezone 

from app.Domain.v1.QR_codes.Models.qr_model import QRCode
from app.Domain.v1.Offices.Models.office_model import Office
from app.Domain.v1.QR_codes.Schemas.qr_schema import (
    GenerateQRCodeRequest,
    GenerateQRCodeResponse,
    QRCodeResponse,
    OfficeInfo
)
from app.Domain.v1.QR_codes.Services.qr_service import (
    generate_qr_code_for_office,
    generate_qr_code_image
)

class QRCodeService:
    """Cleaned Business Logic for QR Management"""

    # Get the office or raise a 404 error
    @staticmethod
    def _get_office_or_404(db: Session, office_id: int) -> Office:
        office = db.query(Office).filter(Office.id == office_id).first()
        if not office:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Office {office_id} not found")
        return office

    # Format the response for the API
    @staticmethod
    def _format_response(qr_record: QRCode, image_b64: str, office: Office) -> GenerateQRCodeResponse:
        return GenerateQRCodeResponse(
            id=qr_record.id,
            office_id=qr_record.office_id,
            qr_token=qr_record.qr_token,
            is_active=qr_record.is_active,
            qr_code_image=f"data:image/png;base64,{image_b64}",
            office=OfficeInfo(id=office.id, name=office.name, public_ip=office.public_ip),
            created_at=qr_record.created_at,
            updated_at=qr_record.updated_at
        )

    # Create a new QR code for a new office
    @staticmethod
    def generate_qr_code(db: Session, request: GenerateQRCodeRequest) -> GenerateQRCodeResponse:
        office = QRCodeService._get_office_or_404(db, request.office_id)
        
        token, _, image = generate_qr_code_for_office(
            office.id, office.name, office.public_ip
        )

        now = datetime.now(timezone.utc)

        qr_code = QRCode(
            office_id=office.id, 
            qr_token=token, 
            is_active=True,
            created_at=now,
            updated_at=now
        )
        
        try:
            db.add(qr_code)
            db.commit()
            db.refresh(qr_code)
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to create QR code: {str(e)}"
            )

        return QRCodeService._format_response(qr_code, image, office)

    # Regenerate the QR token for an existing QR code
    @staticmethod
    def regenerate_qr_token(db: Session, qr_code_id: int) -> GenerateQRCodeResponse:
        qr_code = db.query(QRCode).filter(QRCode.id == qr_code_id).first()
        if not qr_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, "QR record not found")
        
        office = QRCodeService._get_office_or_404(db, qr_code.office_id)
        
        new_token, _, new_image = generate_qr_code_for_office(
            office.id, office.name, office.public_ip
        )

        qr_code.qr_token = new_token
        qr_code.updated_at = datetime.now(timezone.utc)
        
        db.commit()
        db.refresh(qr_code)

        return QRCodeService._format_response(qr_code, new_image, office)

    # Get all QR codes
    @staticmethod
    def get_all_qr_codes(db: Session, skip: int, limit: int, is_active: Optional[bool], office_id: Optional[int]):
        query = db.query(QRCode)
        if is_active is not None: query = query.filter(QRCode.is_active == is_active)
        if office_id is not None: query = query.filter(QRCode.office_id == office_id)
        return query.order_by(QRCode.created_at.desc()).offset(skip).limit(limit).all()

    # Get a QR code by ID
    @staticmethod
    def get_qr_code_by_id(db: Session, qr_code_id: int) -> QRCodeResponse:
        """Get QR code by ID"""
        qr_code = db.query(QRCode).filter(QRCode.id == qr_code_id).first()
        if not qr_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"QR code {qr_code_id} not found")
        
        # Get office information
        office = QRCodeService._get_office_or_404(db, qr_code.office_id) 
        
        return QRCodeResponse(
            id=qr_code.id,
            office_id=qr_code.office_id,
            qr_token=qr_code.qr_token,
            is_active=qr_code.is_active,
            office=OfficeInfo(
                id=office.id,
                name=office.name,
                public_ip=office.public_ip
            ) if office else None,
            created_at=qr_code.created_at,
            updated_at=qr_code.updated_at
        )

    # Get a QR code by token
    @staticmethod
    def get_qr_code_by_token(db: Session, qr_token: str) -> QRCodeResponse:
        """Get QR code by token"""
        qr_code = db.query(QRCode).filter(QRCode.qr_token == qr_token).first()
        if not qr_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"QR code with token '{qr_token}' not found")
        
        # Get office information
        office = QRCodeService._get_office_or_404(db, qr_code.office_id) 
        
        return QRCodeResponse(
            id=qr_code.id,
            office_id=qr_code.office_id,
            qr_token=qr_code.qr_token,
            is_active=qr_code.is_active,
            office=OfficeInfo(
                id=office.id,
                name=office.name,
                public_ip=office.public_ip
            ) if office else None,
            created_at=qr_code.created_at,
            updated_at=qr_code.updated_at
        )

    # Get a QR code image by ID
    @staticmethod
    def get_qr_code_image(db: Session, qr_code_id: int) -> str:
        """Get QR code image by ID (regenerate from token)"""
        qr_code = db.query(QRCode).filter(QRCode.id == qr_code_id).first()
        if not qr_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"QR code {qr_code_id} not found")
        
        # Get office information to regenerate QR code with office data
        office = db.query(Office).filter(Office.id == qr_code.office_id).first()
        if not office:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"Office {qr_code.office_id} not found")
        
        # Regenerate QR code image from stored token and office info
        # CRITICAL: Use the EXISTING token from database, not generate a new one
        _, qr_data_json, qr_image = generate_qr_code_for_office(
            office.id, office.name, office.public_ip, qr_token=qr_code.qr_token
        )
        
        return f"data:image/png;base64,{qr_image}"


    # Delete a QR code
    @staticmethod
    def delete_qr_code(db: Session, qr_code_id: int):
        qr_code = db.query(QRCode).filter(QRCode.id == qr_code_id).first()
        if not qr_code:
            raise HTTPException(status.HTTP_404_NOT_FOUND, f"QR code {qr_code_id} not found")
        
        # Remove redundant check - if we reach here, qr_code exists
        qr_code.is_active = False
        qr_code.updated_at = datetime.now(timezone.utc)
        db.commit()