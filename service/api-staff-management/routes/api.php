<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;
use App\Domain\v1\Auth\Controllers\AuthController;


Route::prefix('internal')->group(function () {
    // This matches: http://api-staff-management/api/internal/verify-credentials
    Route::post('/verify-credentials', [AuthController::class, 'verify']);
});

// Staff routes - will be handled by StaffController later
Route::prefix('staff')->group(function () {
    Route::get('/', function (Request $request) {
        return response()->json([
            'status' => 'success',
            'message' => 'Staff API endpoint',
            'path' => '/api/staff',
        ]);
    });
    
    // Add more staff routes here later
    // Route::get('/', [StaffController::class, 'index']);
    // Route::get('/{id}', [StaffController::class, 'show']);
    // etc.
});