from sqlalchemy import Column, Integer, String, Date, DateTime, Time, ForeignKey, Numeric
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Shared.Infra.database import Base

class Attendance(Base):
    """Model for attendance - matches existing attendances table"""
    __tablename__ = "attendances"

    id = Column(Integer, primary_key=True, index=True)
    # Part of composite index
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    # Has foreign key index
    office_id = Column(Integer, ForeignKey('offices.id', ondelete='CASCADE'), nullable=True, index=True)
    # Has individual + composite index
    log_date = Column(Date, nullable=False, index=True)
    check_in = Column(Time, nullable=True)
    check_out = Column(Time, nullable=True)
    status = Column(String, nullable=False, index=True)  # Has index: attendance_status_index
    minutes_late = Column(Integer, nullable=False, default=0)
    work_hours = Column(Numeric(4, 2), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationships
    attendance_reasons = relationship("AttendanceReason", back_populates='attendance', cascade='all, delete-orphan')
