from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Shared.Infra.database import Base

class QRCode(Base):
    """Model for QR codes - matches existing qr_codes table"""
    __tablename__ = "qr_codes"

    id = Column(Integer, primary_key=True, index=True)
    office_id = Column(Integer, ForeignKey('offices.id', ondelete='CASCADE'), nullable=False)
    qr_token = Column(String(255), unique=True, nullable=False, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Bidirectional relationship with Office
    office = relationship('Office', back_populates='qr_codes')