<?php

namespace App\Domain\v1\Auth\Middleware;

use Closure;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use Illuminate\Support\Facades\Cache;
use Symfony\Component\HttpFoundation\Response;

class AuthenticateGatewaySession
{
    /**
     * Handle an incoming request.
     * 
     * PERFORMANCE OPTIMIZED:
     * - Caches authenticated user to avoid DB queries on every request
     * - Only queries DB if user not in cache
     * - Reuses Redis connection for better performance
     * 
     * This middleware authenticates users based on the gateway's session cookie (g_sid).
     * It reads the session from Redis (shared with gateway) and sets the authenticated user.
     *
     * @param  \Closure(\Illuminate\Http\Request): (\Symfony\Component\HttpFoundation\Response)  $next
     */
    public function handle(Request $request, Closure $next): Response
    {
        // Get the gateway session cookie
        $sessionId = $request->cookie('g_sid');
        
        if (!$sessionId) {
            return response()->json([
                'message' => 'Unauthenticated'
            ], 401);
        }

        try {
            // PERFORMANCE: Check cache first (user already authenticated in this request cycle)
            $cacheKey = "auth_user:{$sessionId}";
            $user = Cache::get($cacheKey);
            
            if ($user) {
                // User found in cache - set and continue (FAST PATH)
                Auth::setUser($user);
                return $next($request);
            }

            // Read session from Redis (same Redis instance as gateway)
            // Gateway stores sessions without Laravel's prefix, so we need raw access
            $redisConfig = config('database.redis.default');
            
            // Use singleton pattern for Redis connection (reuse connection)
            static $redisClient = null;
            if (!$redisClient) {
                $redisClient = new \Redis();
                $redisClient->connect(
                    $redisConfig['host'] ?? '127.0.0.1',
                    $redisConfig['port'] ?? 6379
                );
                
                if (!empty($redisConfig['password'])) {
                    $redisClient->auth($redisConfig['password']);
                }
            }
            
            // Gateway stores sessions without prefix, so read directly
            $sessionData = $redisClient->get("session:{$sessionId}");
            
            if (!$sessionData) {
                return response()->json([
                    'message' => 'Session expired'
                ], 401);
            }

            // Parse session data
            $data = json_decode($sessionData, true);
            $userId = $data['user_id'] ?? $sessionData; // Fallback for old format

            if (!$userId) {
                return response()->json([
                    'message' => 'Invalid session'
                ], 401);
            }

            // PERFORMANCE: Cache user lookup (5 minutes) to avoid DB query on every request
            $user = Cache::remember("user:{$userId}", 300, function () use ($userId) {
                return \App\Domain\v1\Users\Models\User::find($userId);
            });
            
            if (!$user) {
                return response()->json([
                    'message' => 'User not found'
                ], 401);
            }

            // PERFORMANCE: Cache authenticated user for this session (until session expires)
            // This avoids Redis lookup + DB query on subsequent requests
            Cache::put($cacheKey, $user, 300); // 5 minutes (matches session refresh)

            // Set the authenticated user
            Auth::setUser($user);
            
        } catch (\Exception $e) {
            // Log error for debugging but don't expose details
            \Log::error('Gateway auth failed', [
                'session_id' => $sessionId ?? 'none',
                'error' => $e->getMessage()
            ]);
            
            return response()->json([
                'message' => 'Authentication failed'
            ], 401);
        }

        return $next($request);
    }
}

