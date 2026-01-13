<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Domain\v1\Auth\Controllers\AuthController;
use App\Domain\v1\Staffs\Controllers\StaffController;
use App\Domain\v1\Attendance_Records\Controllers\AttendanceHistoryController;

Route::prefix('internal')->group(function () {
    // This matches: http://api-staff-management/api/internal/verify-credentials
    Route::post('/verify-credentials', [AuthController::class, 'verify']);

    // Get authenticated user profile with full staff details
    Route::post('/me', [AuthController::class, 'me']);
});

// Staff routes - will be handled by StaffController later

Route::middleware('gateway.auth')->prefix('staff')->group(function () {
    Route::get('/', [StaffController::class, 'index']);
    Route::post('/', [StaffController::class, 'store']);
    Route::put('/{id}', [StaffController::class, 'update']);
    Route::delete('/{id}', [StaffController::class, 'destroy']);
});

// Attendance History routes
Route::middleware('gateway.auth')->prefix('attendance-records')->group(function () {
    Route::get('/', [AttendanceHistoryController::class, 'index']);
    Route::get('/statistics', [AttendanceHistoryController::class, 'statistics']);
    Route::get('/export', [AttendanceHistoryController::class, 'export']);
});
// GET /api/attendance/history          - Paginated history with filters
// GET /api/attendance/statistics       - Monthly statistics
// GET /api/attendance/export           - Download Excel