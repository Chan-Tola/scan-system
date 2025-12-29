from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from typing import Generator
from app.Shared.Core.config import settings

DATABASE_URL = f"postgresql://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}"

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
    echo=settings.DEBUG
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Generator[Session, None, None]:
    """Database session dependency"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# def init_db():
#     """Initialize database tables"""
#     # Import all models here
#     from app.Domain.v1.QR_codes.models import QRCode
#     from app.Domain.v1.Attendences.models import Attendance
#     from app.Domain.v1.Offices.models import Office
#     from app.Domain.v1.Attendence_reasons.models import AttendanceReason
    
#     Base.metadata.create_all(bind=engine)