export interface DailyStats {
  date: string
  total_staff: number
  active_staff: number
  absent_staff: number
  on_time_count: number
  late_count: number
}

export interface MonthlyTrendPoint {
  date: string
  on_time_percentage: number
  late_percentage: number
  absent_percentage: number
  total_staff: number
}

export interface MonthlyTrend {
  month: string
  data_points: MonthlyTrendPoint[]
}

export interface DashboardData {
  daily_stats: DailyStats
  monthly_trend: MonthlyTrend
}