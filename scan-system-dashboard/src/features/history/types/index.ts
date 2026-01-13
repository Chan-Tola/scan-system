export type HistoryFilters = {
  name?: string
  status?: 'on_time' | 'late' | 'absent' | 'present'
  month?: string // YYYY-MM format
  page?: number
  per_page?: number
}

export type HistoryRecord = {
  id: number
  staff_name: string
  office_name: string
  log_date: string
  check_in: string | null
  check_out: string | null
  status: string
  minutes_late: number
  work_hours: number | null
  stop_count: number
  reasons: Array<{
    id: number
    reason_type: string
    reason: string
  }>
  created_at: string
}

export type HistoryListResponse = {
  status: string
  data: HistoryRecord[]
  pagination: {
    current_page: number
    total: number
    last_page: number
    per_page: number
  }
}

export type StatisticsResponse = {
  status: string
  data: {
    month: string
    on_time_count: number
    late_count: number
    absent_count: number
    total_records: number
  }
}
