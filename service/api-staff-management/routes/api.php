<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Domain\v1\Auth\Controllers\AuthController;
use App\Domain\v1\Staffs\Controllers\StaffController;

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

    Route::get('/test/cloudinary', [StaffController::class, 'testCloudinary']);
});
