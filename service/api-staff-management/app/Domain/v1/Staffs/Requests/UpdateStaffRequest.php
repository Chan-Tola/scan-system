<?php

namespace App\Domain\v1\Staffs\Requests;

use App\Domain\v1\Staffs\Models\Staff;
use App\Domain\v1\Users\Models\User;
use Illuminate\Foundation\Http\FormRequest;
use Illuminate\Validation\Rule;

class UpdateStaffRequest extends FormRequest
{
    public function authorize(): bool
    {
        return true;
    }

    public function rules(): array
    {
        $staffId = $this->route('id');
        $staff = Staff::find($staffId);
        $userId = $staff ? $staff->user_id : null;

        return [
            // User Fields (optional on update)
            User::USERNAME => [
                'sometimes',
                'required',
                'string',
                'max:255',
                Rule::unique('users', 'username')->ignore($userId)
            ],
            User::EMAIL => [
                'sometimes',
                'required',
                'email',
                'max:255',
                Rule::unique('users', 'email')->ignore($userId)
            ],
            User::PASSWORD => 'sometimes|nullable|string|min:8|confirmed',

            // Staff fields
            Staff::OFFICE_ID => 'sometimes|required|exists:offices,id',
            Staff::FULL_NAME => 'sometimes|required|string|max:255',
            Staff::GENDER => 'nullable|in:male,female,other',
            Staff::PHONE => 'nullable|string|max:20',
            Staff::ADDRESS => 'nullable|string',
            Staff::DATE_OF_BIRTH => 'nullable|date',
            Staff::JOIN_DATE => 'nullable|date',
            Staff::SHIFT_START => 'sometimes|required|date_format:H:i:s',
            Staff::SHIFT_END => 'sometimes|required|date_format:H:i:s|after:shift_start',
            Staff::PROFILE_IMAGE => 'nullable|image|mimes:jpeg,png,jpg,gif|max:5120',
        ];
    }

    public function messages(): array
    {
        return [
            User::USERNAME . '.unique' => 'Username already exists',
            User::EMAIL . '.email' => 'Email must be a valid email address',
            User::EMAIL . '.unique' => 'Email already exists',
            User::PASSWORD . '.min' => 'Password must be at least 8 characters',
            User::PASSWORD . '.confirmed' => 'Password confirmation does not match',
            Staff::OFFICE_ID . '.exists' => 'Selected office does not exist',
            Staff::SHIFT_END . '.after' => 'Shift end time must be after shift start time',
        ];
    }
}
