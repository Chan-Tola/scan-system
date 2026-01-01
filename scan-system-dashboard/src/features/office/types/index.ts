export interface Office {
    id: number
    name: string
    public_ip: string
}

export interface OfficeResponse {
    status: string
    data: Office | Office[]
    message?: string
}

export interface OfficeCreate {
    name: string
    public_ip?: string
}

export interface OfficeUpdate {
    name?: string
    public_ip?: string
}
  