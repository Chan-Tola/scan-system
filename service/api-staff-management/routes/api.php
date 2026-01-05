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
Route::prefix('staff')->group(function () {
    Route::get('/', [StaffController::class, 'index']);
    Route::post('/', [StaffController::class, 'store']);
    Route::delete('/{id}', [StaffController::class, 'destroy']);
    Route::post('/{id}', [StaffController::class, 'update']); // Using POST for file upload spoofing if needed, but Laravel supports PUT with _method field. Let's start with direct PUT first or use POST to avoid multipart/form-data issues with PUT. Better use POST with /{id} for file uploads in PHP.

    // Test Cloudinary endpoint
    Route::get('/test/cloudinary', [StaffController::class, 'testCloudinary']);
});
