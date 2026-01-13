<?php

namespace App\Domain\v1\Attendance_Records\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class AttendanceHistoryResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     */
    public function toArray($request): array
    {
        return [
            'id' => $this->id,
            'staff_name' => $this->user?->staff?->full_name ?? 'N/A',
            'office_name' => $this->office?->name ?? 'N/A',
            'log_date' => $this->log_date?->format('Y-m-d') ?? null,
            'check_in' => $this->check_in ? date('H:i:s', strtotime($this->check_in)) : null,
            'check_out' => $this->check_out ? date('H:i:s', strtotime($this->check_out)) : null,
            'status' => $this->status,
            'minutes_late' => $this->minutes_late ?? 0,
            'work_hours' => $this->work_hours ? (float) $this->work_hours : null,
            'stop_count' => $this->stop_count ?? 0,
            'reasons' => $this->reasons->map(function ($reason) {
                return [
                    'id' => $reason->id,
                    'reason_type' => $reason->reason_type,
                    'reason' => $reason->reason,
                ];
            }),
            'created_at' => $this->created_at?->format('Y-m-d H:i:s'),
        ];
    }
}

