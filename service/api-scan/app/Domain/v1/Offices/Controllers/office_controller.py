from sqlalchemy.orm import Session
from fastapi import HTTPException, status
from typing import List, Optional
from datetime import datetime
from app.Domain.v1.Offices.Models.office_model import Office
from app.Domain.v1.Offices.Schemas.office_schema import OfficeCreate, OfficeUpdate

class OfficeService:
    """Service layer for office business logic"""
    @staticmethod
    def get_all_offices(db: Session, skip: int = 0, limit: int = 100) -> List[Office]:
        """Get all offices"""
        return db.query(Office).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_office_by_id(db: Session, office_id: int) -> Office:
        """ Get office by ID """
        office = db.query(Office).filter(Office.id == office_id).first()

        if not office:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Office with id {office_id} not found"
            )
        return office

    @staticmethod
    def create_office(db: Session, office_data: OfficeCreate) -> Office:
        """ Create a new office """
        now = datetime.utcnow()
        new_office = Office(**office_data.model_dump())
        new_office.created_at = now
        new_office.updated_at = now
        db.add(new_office)
        db.commit()
        db.refresh(new_office)
        return new_office
    
    @staticmethod
    def update_office(db: Session, office_id: int, office_data: OfficeUpdate) -> Office:
        """Update an existing office"""
        db_office = OfficeService.get_office_by_id(db, office_id)

        update_data = office_data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_office, key, value)

        # Set updated_at timestamp
        db_office.updated_at = datetime.utcnow()

        db.commit()
        db.refresh(db_office)
        return db_office
    
    @staticmethod
    def delete_office(db: Session, office_id: int) -> None:
        """ Delete an office by ID """
        db_office = OfficeService.get_office_by_id(db, office_id)
        db.delete(db_office)
        db.commit()
        return None

