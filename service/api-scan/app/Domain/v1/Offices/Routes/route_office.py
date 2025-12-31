from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List
from app.Shared.Infra.database import get_db
from app.Domain.v1.Offices.Schemas.office_schema import OfficeResponse, OfficeCreate, OfficeUpdate
from app.Domain.v1.Offices.Controllers.office_controller import OfficeService

router = APIRouter(prefix="/offices", tags=["Offices"])

@router.get("/", response_model=List[OfficeResponse])
def get_all_offices(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """ Get all offices """
    offices = OfficeService.get_all_offices(db, skip=skip, limit=limit)
    return offices

@router.get("/{office_id}", response_model=OfficeResponse)
def get_office(office_id: int, db: Session = Depends(get_db)):
    """ Get office data by id """
    return OfficeService.get_office_by_id(db, office_id)

@router.post("/", response_model=OfficeResponse, status_code=status.HTTP_201_CREATED)
def create_office(office: OfficeCreate, db: Session = Depends(get_db)):
    """ Create a new office """
    return OfficeService.create_office(db, office)

@router.put("/{office_id}", response_model=OfficeResponse)
def update_office(office_id: int, office: OfficeUpdate, db: Session = Depends(get_db)):
    """Update an existing office"""
    return OfficeService.update_office(db, office_id, office)

@router.delete("/{office_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_office(office_id: int, db: Session = Depends(get_db)):
    """Delete an office"""
    OfficeService.delete_office(db, office_id)
    return None