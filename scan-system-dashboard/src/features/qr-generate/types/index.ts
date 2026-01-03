export interface OfficeInfo {
  id: number
  name: string
  public_ip: string
}
export interface QRCode {
  id: number
  office_id: number
  qr_token: string
  is_active: boolean
  office: OfficeInfo | null
  created_at: string | null
  updated_at: string | null
}

export interface GenerateQRCodeRequest {
  office_id: number
}

export interface GenerateQRCodeResponse {
  id: number
  office_id: number
  qr_token: string
  is_active: boolean
  qr_code_image: string // Base64 encoded image
  office: OfficeInfo
  created_at: string | null
  updated_at: string | null
}

export interface QRCodeResponse {
  id: number
  office_id: number
  qr_token: string
  is_active: boolean
  office: OfficeInfo | null
  created_at: string | null
  updated_at: string | null
}
