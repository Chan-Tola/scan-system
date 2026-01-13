<?php

namespace App\Domain\v1\Attendance_Records\Requests;

use Illuminate\Foundation\Http\FormRequest;

class AttendanceHistoryRequest extends FormRequest
{
    /**
     * Determine if the user is authorized to make this request.
     */
    public function authorize(): bool
    {
        return true; // Authorization handled by middleware
    }

    /**
     * Get the validation rules that apply to the request.
     */
    public function rules(): array
    {
        return [
            'name' => 'nullable|string|max:255',
            'status' => 'nullable|in:on_time,late,absent,present',
            'month' => 'nullable|date_format:Y-m',
            'per_page' => 'nullable|integer|min:1|max:100',
            'page' => 'nullable|integer|min:1',
        ];
    }

    /**
     * Get custom messages for validator errors.
     */
    public function messages(): array
    {
        return [
            'status.in' => 'Status must be one of: on_time, late, absent, present',
            'month.date_format' => 'Month must be in YYYY-MM format (e.g., 2026-01)',
            'per_page.max' => 'Maximum items per page is 100',
        ];
    }

    /**
     * Get validated data with defaults
     */
    public function validated($key = null, $default = null)
    {
        $validated = parent::validated();

        // Set defaults
        $validated['per_page'] = $validated['per_page'] ?? 15;
        $validated['page'] = $validated['page'] ?? 1;

        return $key ? ($validated[$key] ?? $default) : $validated;
    }
}

