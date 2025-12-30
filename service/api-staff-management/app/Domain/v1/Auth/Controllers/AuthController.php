<?php

namespace App\Domain\v1\Auth\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;

class AuthController extends Controller
{
    public function verify(Request $request)
    {
        // validate request
        $credentials = $request->validate([
            'email' => 'required|email',
            'password' => 'required|string',
        ]);

        // Attempt Authentication
        // Auth::once() checks the DB but does NOT create a Laravel session cookie
        if(Auth::once($credentials))
        {
            $user = Auth::user();

            // return user data to gateway (Status 208 = Already Reported - used for internal verification)
            return response()->json([
                'id'    => $user->id,
                'email' => $user->email,
                'username'  => $user->username,
            ], 208);
        }

        // Fail
        return response()->json([
            'message' => 'Invalid staff credentials'
        ], 401);
    }
}