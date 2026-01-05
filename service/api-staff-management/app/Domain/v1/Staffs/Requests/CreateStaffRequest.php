<?php

namespace App\Domain\v1\Staffs\Requests;

use App\Domain\v1\Users\Models\User;
use App\Domain\v1\Staffs\Models\Staff;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class CreateStaffRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        return [
            // User Fields
            User::USERNAME => 'required|string|max:255|unique:users,username',
            User::EMAIL => 'required|email|max:255|unique:users,email',
            User::PASSWORD => 'required|string|min:8',
            'role' => 'required|string|exists:roles,name',

            // Staff fields
            Staff::OFFICE_ID => 'required|exists:offices,id',
            Staff::FULL_NAME => 'required|string|max:255',
            Staff::GENDER => 'nullable|in:male,female,other',
            Staff::PHONE => 'nullable|string|max:20',
            Staff::ADDRESS => 'nullable|string',
            Staff::DATE_OF_BIRTH => 'nullable|date',
            Staff::JOIN_DATE => 'nullable|date',
            Staff::SHIFT_START => 'nullable|date_format:H:i:s',
            Staff::SHIFT_END => 'nullable|date_format:H:i:s|after:shift_start',
            Staff::PROFILE_IMAGE => 'nullable|image|mimes:jpeg,png,jpg,gif|max:10240', // 10MB max
        ];
    }

    public function messages(): array
    {
        return [
            User::USERNAME . '.required' => 'Username is required',
            User::USERNAME . '.unique' => 'Username already exists',
            User::EMAIL . '.required' => 'Email is required',
            User::EMAIL . '.email' => 'Email must be a valid email address',
            User::EMAIL . '.unique' => 'Email already exists',
            User::PASSWORD . '.required' => 'Password is required',
            User::PASSWORD . '.min' => 'Password must be at least 8 characters',
            User::PASSWORD . '.confirmed' => 'Password confirmation does not match',
            Staff::OFFICE_ID . '.required' => 'Office ID is required',
            Staff::OFFICE_ID . '.exists' => 'Selected office does not exist',
            Staff::FULL_NAME . '.required' => 'Full name is required',
            Staff::SHIFT_END . '.after' => 'Shift end time must be after shift start time',
        ];
    }
}
