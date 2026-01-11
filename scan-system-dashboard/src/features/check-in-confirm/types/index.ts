export interface CheckOutRequest {
  qr_token?: string
  reason_type?: 'early_leave'
  reason?: string
}
export interface CheckOutResponse {
  message: string
  attendance: {
    id: number
    user_id: number
    office_id: number
    log_date: string
    check_in: string
    check_out: string
    status: string
    minutes_late: number
    work_hours: number
    office: {
      id: number
      name: string
      public_ip: string | null
    }
  }
  work_hours: number
  is_early_leave: boolean
}
export interface TodayAttendanceResponse {
  id: number
  user_id: number
  office_id: number
  log_date: string
  check_in: string | null
  check_out: string | null
  status: string
  minutes_late: number
  work_hours: number | null
  office: {
    id: number
    name: string
    shift_start: string
    shift_end: string
  }
}
