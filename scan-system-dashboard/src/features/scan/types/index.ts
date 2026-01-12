// QR Validate Request
export interface QRValidationRequest {
  qr_token: string
  client_ip?: string
}

// Office
export interface OfficeInfo {
  id: number
  name: string
  public_ip: string | null
}

// QR Validate Response
export interface QRValidationResponse {
  valid: boolean
  message: string
  office?: OfficeInfo
}

// Check In Request
export interface CheckInRequest {
  qr_token: string
  client_ip?: string
}

// Check In Response
export interface CheckInResponse {
  message: string
  attendance: {
    id: number
    user_id: number
    office_id: number
    log_date: string
    check_in: string
    status: string
    minutes_late: number
    office: OfficeInfo
  }
  is_late: boolean
  minutes_late: number
}

// Check Out Request
export interface CheckOutRequest {
  qr_token?: string
  reason_type?: 'early_leave'
  reason?: string
}

// Check Out Response
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

//  Get the TodayAttendanceResponse From Backend For Button Check Out
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

// Permission Request For Absent
export interface PermissionRequest {
  date: string // Date of absence (YYYY-MM-DD)
  reason_type: string // 'absent' | 'sick' | 'personal' | 'emergency'
  reason: string // Detailed reason text
}

// Permission Response For Absent
export interface PermissionResponse {
  message: string
  attendance: {
    id: number
    user_id: number
    log_date: string
    status: string // 'absent'
    created_at: string
  }
  attendance_reason: {
    id: number
    attendance_id: number
    reason_type: string
    reason: string
    created_at: string
  }
}
