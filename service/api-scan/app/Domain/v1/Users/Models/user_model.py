from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.Shared.Infra.database import Base

class User(Base):
    """User model matching Laravel api-staff-management service
    Note: User management (CRUD) is handled by api-staff-management service.
    This model is for foreign key reference and read-only queries in api-scan service.
    """

    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    email_verified_at = Column(DateTime(timezone=True), nullable=True)
    password = Column(String, nullable=False)
    remember_token = Column(String(100), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=True)
    updated_at = Column(DateTime(timezone=True), nullable=True)

    # Relationship (optional - one-way since Attendance doesn't back_populate to user)
    attendances = relationship("Attendance", backref="user", lazy="dynamic")