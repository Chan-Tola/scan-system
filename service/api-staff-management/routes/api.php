<?php

use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;


Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');


Route::get('/', function (Request $request) {
    return response()->json([
        'status' => 'success',
        'message' => 'Hello from Laravel 11 + FrankenPHP!',
        'timestamp' => now()->toDateTimeString(),
        'server' => 'Octane/FrankenPHP'
    ]);
});
