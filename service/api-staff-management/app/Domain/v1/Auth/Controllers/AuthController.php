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
        // Validate request - accept identifier (username or email)
        $validated = $request->validate([
            'identifier' => 'required|string',
            'password' => 'required|string',
        ]);

        // Determine if identifier is email or username
        $fieldType = filter_var($validated['identifier'], FILTER_VALIDATE_EMAIL) ? 'email' : 'username';
        
        // Build credentials array for authentication
        $credentials = [
            $fieldType => $validated['identifier'],
            'password' => $validated['password'],
        ];

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
            'message' => 'Invalid credentials'
        ], 401);
    }

    public function me(Request $request)
    {
        $userId = $request->input('user_id');

        // 1. Fetch Staff with User, Office, and User Roles
        $staff = \App\Domain\v1\Staffs\Models\Staff::with([
            'user' => function ($q) {
                // Select only specific user columns and their role names
                $q->select('id', 'email', 'username')->with('roles:id,name');
            },
            'office:id,name'
        ])
            ->select(
                'id',
                'user_id',
                'office_id',
                'full_name',
                'gender',
                'phone',
                'address',
                'profile_image',
                'date_of_birth',
                'shift_start',
                'shift_end'
            )
            ->where('user_id', $userId)
            ->first();


        if (!$staff) {
            $user = \App\Domain\v1\Users\Models\User::with('roles:id,name')
                ->select('id', 'email', 'username')
                ->find($userId);

            if (!$user) return response()->json(['message' => 'Not found'], 404);

            return response()->json([
                'id'       => $user->id,
                'email'    => $user->email,
                'username' => $user->username,
                'role'     => $user->roles->first()?->name ?? 'user',
                'profile'  => null
            ], 200);
        }


        return response()->json([
            'id'       => $staff->user->id,
            'email'    => $staff->user->email,
            'username' => $staff->user->username,
            'role'     => $staff->user->roles->first()?->name ?? 'staff',
            'profile'  => $staff
        ], 200);
    }
}
