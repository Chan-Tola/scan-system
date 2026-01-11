/**
 * Get user's public IP address using backend endpoint
 * Backend calls ipify.org API (more secure and reliable than client-side)
 * 
 * Performance optimization: Caches IP in sessionStorage to avoid repeated API calls
 * Cache expires after 5 minutes (IPs rarely change during a session)
 */
import axios from 'axios'

const CACHE_KEY = 'user_public_ip'
const CACHE_EXPIRY_MS = 5 * 60 * 1000 // 5 minutes

interface CachedIp {
  ip: string
  timestamp: number
}

interface PublicIpResponse {
  ip: string | null
  success: boolean
  message?: string | null
}

// Create axios instance for API calls (same as attendanceApi.ts)
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
  withCredentials: true,
})

export async function getPublicIp(): Promise<string | null> {
  // Check cache first (performance optimization)
  try {
    const cached = sessionStorage.getItem(CACHE_KEY)
    if (cached) {
      const cachedData: CachedIp = JSON.parse(cached)
      const now = Date.now()
      
      // Use cached IP if still valid (within 5 minutes)
      if (now - cachedData.timestamp < CACHE_EXPIRY_MS) {
        console.log('Using cached public IP:', cachedData.ip)
        return cachedData.ip
      } else {
        // Cache expired, remove it
        sessionStorage.removeItem(CACHE_KEY)
      }
    }
  } catch (error) {
    // If cache fails, continue to fetch
    console.warn('Failed to read IP cache:', error)
  }
  
  // Fetch from backend endpoint
  try {
    const response = await api.get<PublicIpResponse>('/api/scan/get-public-ip')
    
    if (response.data.success && response.data.ip) {
      const ip = response.data.ip
      
      // Cache the IP for future requests
      try {
        const cacheData: CachedIp = {
          ip,
          timestamp: Date.now()
        }
        sessionStorage.setItem(CACHE_KEY, JSON.stringify(cacheData))
      } catch (cacheError) {
        // If caching fails, continue (non-critical)
        console.warn('Failed to cache IP:', cacheError)
      }
      
      return ip
    } else {
      console.error('Failed to get public IP from backend:', response.data.message)
      return null
    }
  } catch (error) {
    console.error('Failed to get public IP from backend endpoint:', error)
    return null
  }
}

