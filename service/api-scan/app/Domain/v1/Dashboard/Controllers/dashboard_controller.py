from sqlalchemy.orm import Session
from sqlalchemy import func, case
from datetime import date, timedelta
from typing import List
from app.Domain.v1.Attendances.Models.attendance_model import Attendance
from app.Domain.v1.Dashboard.Schemas.dashboard_schema import (
    DailyStats,
    MonthlyTrendPoint,
    MonthlyTrend,
    DashboardResponse
)

class DashboardService:
    """Business Logic for Dashboard"""
    @staticmethod
    def _get_daily_stats(db: Session) -> DailyStats:
        """ 
            Get today's attendance statistics
            Single optimized query with aggregations
        """
        today = date.today()

        # Single aggregation query  ( FAST! )
        result = db.query(
            func.count(Attendance.id).label("total"),
            func.sum(case((Attendance.status == 'on_time', 1), else_=0)).label('on_time'),
            func.sum(case((Attendance.status == 'late', 1), else_=0)).label('late'),
            func.sum(case((Attendance.status == 'absent', 1), else_=0)).label('absent')
        ).filter(Attendance.log_date == today).first()

        # Calculate total staff
        on_time = result.on_time or 0
        late = result.late or 0
        absent = result.absent or 0
        total = result.total or 0

        stats = DailyStats(
            date=str(today),
            total_staff=total,
            active_staff=on_time + late,
            absent_staff=absent,
            on_time_count=on_time,
            late_count=late
        )

        return stats

    @staticmethod
    def _get_monthly_trend(db: Session, year: int, month: int) -> MonthlyTrend :
        """ 
            Get monthly trend with daily percentages
            Single query grouped by date
        """

        # Get First and last day of month
        first_day = date(year, month, 1)
        if month == 12:
            last_day = date(year + 1, 1, 1) - timedelta(days=1)
        else:
            last_day = date(year, month + 1, 1) - timedelta(days=1)

        # Query all days in month (single query with GROUP BY)
        results = db.query(
            Attendance.log_date,
            func.count(Attendance.id).label("total"),
            func.sum(case((Attendance.status == 'on_time', 1), else_=0)).label('on_time'),
            func.sum(case((Attendance.status == 'late',1), else_=0)).label('late'),
            func.sum(case((Attendance.status == 'absent',1), else_=0)).label('absent')
        ).filter(
            Attendance.log_date >= first_day,
            Attendance.log_date <= last_day
        ).group_by(
            Attendance.log_date
        ).order_by(
            Attendance.log_date
        ).all()

        # Calculate percentages for each day
        data_points: List[MonthlyTrendPoint] = []
        for row in results:
            total = row.total or 0
            on_time = row.on_time or 0
            late = row.late or 0
            absent = row.absent or 0

            # Avoid division by zero
            if total > 0:
                on_time_pct = round((on_time / total) * 100, 2)
                late_pct = round((late / total) * 100, 2)
                absent_pct = round((absent / total) * 100, 2)
            else:
                on_time_pct = 0.0
                late_pct = 0.0
                absent_pct = 0.0

            data_points.append(MonthlyTrendPoint(
                date=str(row.log_date),
                on_time_percentage=on_time_pct,
                late_percentage=late_pct,
                absent_percentage=absent_pct,
                total_staff=total,
            ))

        trend = MonthlyTrend(
            month=f"{year}-{month:02d}",
            data_points=data_points
        )

        return trend

    @staticmethod
    def _get_dashboard(db: Session) -> DashboardResponse:
        """
            Get Complete dashboard data for today
            - Daily Stats for today
            - Monthly Trend for current month
        """
        today = date.today()

        # Get daily stats
        daily_stats = DashboardService._get_daily_stats(db)

        # Get current month trend
        monthly_trend = DashboardService._get_monthly_trend(db, today.year, today.month)
        
        return DashboardResponse(
            daily_stats=daily_stats,
            monthly_trend=monthly_trend
        )

    
    