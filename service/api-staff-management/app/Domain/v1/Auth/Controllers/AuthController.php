<?php

namespace App\Domain\v1\Auth\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Auth;
use App\Domain\v1\Staffs\Models\Staff;

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
        if (Auth::once($credentials)) {
            $user = Auth::user();

            // return user data to gateway (Status 208 = Already Reported - used for internal verification)
            return response()->json([
                'id'       => $user->id,
                'email'    => $user->email,
                'username' => $user->username,
            ], 208);
        }

        // Fail
        return response()->json([
            'message' => 'Invalid staff credentials'
        ], 401);
    }

    public function me(Request $request)
    {
        $userId = $request->input('user_id');

        // Optimized query: Select only needed columns for speed
        $staff = \App\Domain\v1\Staffs\Models\Staff::with(['user:id,email,username', 'office:id,name'])
            ->select(
                'id',
                'user_id',
                'office_id',
                'full_name',
                'gender',
                'phone',
                'address',
                'profile_image',
                'shift_start',
                'shift_end'
            )
            ->where('user_id', $userId)
            ->first();

        if (!$staff) {
            $user = \App\Domain\v1\Users\Models\User::select('id', 'email', 'username')->find($userId);
            if (!$user) return response()->json(['message' => 'Not found'], 404);

            return response()->json([
                'id'       => $user->id,
                'email'    => $user->email,
                'username' => $user->username,
                'profile'  => null
            ], 200);
        }

        return response()->json([
            'id'       => $staff->user->id,
            'email'    => $staff->user->email,
            'username' => $staff->user->username,
            'profile'  => $staff
        ], 200);
    }
}
