from pydantic import BaseModel
from typing import List
from datetime import date

# Daily Statistics Schema
class DailyStats(BaseModel):
    """ Today's attendance statistics """
    date:str
    total_staff:int
    active_staff:int
    absent_staff:int
    on_time_count:int
    late_count:int
    
# Monthly Trend Point Schema
class MonthlyTrendPoint(BaseModel):
    """ Single data point for monthly trend """
    date: str
    on_time_percentage: float
    late_percentage: float
    absent_percentage: float
    total_staff: int

class MonthlyTrend(BaseModel):
    """ Monthly attendance trend data """
    month: str # YYYY-MM
    data_points: List[MonthlyTrendPoint]

class DashboardResponse(BaseModel):
    """ Complete dashboard data """
    daily_stats:DailyStats
    monthly_trend:MonthlyTrend

