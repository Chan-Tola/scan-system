export interface QRValidationRequest {
  qr_token: string
  client_ip?: string
}

export interface OfficeInfo {
  id: number
  name: string
  public_ip: string | null
}

export interface QRValidationResponse {
  valid: boolean
  message: string
  office?: OfficeInfo
}

export interface CheckInRequest {
  qr_token: string
  client_ip?: string
}

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

export interface PermissionRequest {
  reasonType: string
  reason: string
}
