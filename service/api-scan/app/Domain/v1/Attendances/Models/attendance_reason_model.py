from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Shared.Infra.database import Base

class AttendanceReason(Base):
    """Model for attendance reasons - match existing attendance_reasons table"""
    __tablename__ = "attendance_reasons"

    id = Column(Integer, primary_key=True, index=True)
    # Has index: attendance_reasons_attendance_id_index
    attendance_id = Column(Integer, ForeignKey('attendances.id', ondelete='CASCADE'), nullable=False, index=True)
    # Has index: attendance_reasons_type_index
    reason_type = Column(String, nullable=False, index=True)
    reason = Column(Text, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attendance = relationship("Attendance", back_populates="attendance_reasons")
    