import { Home, QrCode, ScanLine, Building2, Users, Settings, History } from 'lucide-vue-next'
// roles?: Array<'admin' | 'staff'>

export type SidebarItem = {
  title: string
  url: string
  icon: any
}

export const mainItems: SidebarItem[] = [
  { title: 'Dashboard', url: '/dashboard', icon: Home },
  { title: 'Generate QR', url: '/qr-generate', icon: QrCode },
  { title: 'Attendance', url: '/attendance', icon: ScanLine },
]

export const managementItems: SidebarItem[] = [
  { title: 'Office Management', url: '/office', icon: Building2 },
  { title: 'Staff Members', url: '/staff', icon: Users },
  { title: 'Attendance Records', url: '/attendance-records', icon: History },
]

export const settingItems: SidebarItem[] = [{ title: 'Settings', url: '/setting', icon: Settings }]
