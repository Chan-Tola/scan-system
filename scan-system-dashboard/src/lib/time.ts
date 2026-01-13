// src/utils/time.ts
import { format } from 'date-fns'
import { toZonedTime } from 'date-fns-tz'

export const DEFAULT_TIME_ZONE = 'Asia/Phnom_Penh'

/**
 * Format backend "HH:mm:ss" (or "HH:mm") into "hh:mm a" with timezone.
 * Example: "13:07:36" -> "01:07 PM"
 */
export function formatTime(
  time?: string | null,
  options?: {
    timeZone?: string
    pattern?: string
  }
) {
  if (!time) return '-'

  const timeZone = options?.timeZone ?? DEFAULT_TIME_ZONE
  const pattern = options?.pattern ?? 'hh:mm a'

  // normalize "HH:mm" -> "HH:mm:00"
  const normalized = time.length === 5 ? `${time}:00` : time

  // parse as UTC baseline then convert to timezone
  const date = new Date(`1970-01-01T${normalized}Z`)
  const zoned = toZonedTime(date, timeZone)

  return format(zoned, pattern)
}
