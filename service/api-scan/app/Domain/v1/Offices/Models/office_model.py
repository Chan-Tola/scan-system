from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.Shared.Infra.database import Base


class Office(Base):
    __tablename__ = "offices"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    public_ip = Column(String, nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
