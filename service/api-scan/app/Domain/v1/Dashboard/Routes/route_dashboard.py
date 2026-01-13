from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.Shared.Infra.database import get_db
from app.Domain.v1.Dashboard.Schemas.dashboard_schema import (
    DailyStats,
    MonthlyTrend,
    DashboardResponse
)
from app.Domain.v1.Dashboard.Controllers.dashboard_controller import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])

@router.get("/daily-stats", response_model=DailyStats, status_code=status.HTTP_200_OK)
def get_daily_stats(db: Session = Depends(get_db)):

    """
    Get today's attendance statistics
    
    Returns:
    - total_staff: Total attendance records today
    - active_staff: Staff who checked in (on_time + late)
    - absent_staff: Staff marked as absent
    - on_time_count: Staff who came on time
    - late_count: Staff who came late
    """
    
    return DashboardService._get_daily_stats(db)

@router.get("/monthly-trend", response_model=MonthlyTrend, status_code=status.HTTP_200_OK)
def get_monthly_trend(
    year: int,
    month: int,
    db: Session = Depends(get_db)
):
    """
    Get monthly attendance trend with daily percentages
    
    Query params:
    - year: Year (e.g., 2026)
    - month: Month (1-12)
    
    Returns:
    - List of daily data points with percentages
    """
    return DashboardService._get_monthly_trend(db, year, month)

@router.get("/", response_model=DashboardResponse, status_code=status.HTTP_200_OK)
def get_dashboard(db: Session = Depends(get_db)):
    """
    Get complete dashboard data
    
    Returns:
    - daily_stats: Today's statistics
    - monthly_trend: Current month's trend data
    """
    return DashboardService._get_dashboard(db)