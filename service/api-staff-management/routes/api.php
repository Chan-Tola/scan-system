<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Domain\v1\Auth\Controllers\AuthController;
use App\Domain\v1\Staffs\Controllers\StaffController;

Route::prefix('internal')->group(function () {
    // This matches: http://api-staff-management/api/internal/verify-credentials
    Route::post('/verify-credentials', [AuthController::class, 'verify']);
});

// Staff routes - will be handled by StaffController later
Route::prefix('staff')->group(function () {
    Route::get('/', [StaffController::class, 'index']);
    Route::post('/', [StaffController::class, 'store']);
    Route::delete('/{id}', [StaffController::class, 'destroy']);

    // Test Cloudinary endpoint
    Route::get('/test/cloudinary', [StaffController::class, 'testCloudinary']);
});
