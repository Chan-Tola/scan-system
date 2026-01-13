<?php

namespace App\Domain\v1\Attendance_Records\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class MonthlyStatisticsResource extends JsonResource
{
    /**
     * Transform the resource into an array.
     */
    public function toArray($request): array
    {
        // $this->resource is the array from getStatistics()
        return [
            'month' => $this->resource['month'] ?? null,
            'on_time_count' => $this->resource['on_time_count'] ?? 0,
            'late_count' => $this->resource['late_count'] ?? 0,
            'absent_count' => $this->resource['absent_count'] ?? 0,
            'total_records' => $this->resource['total_records'] ?? 0,
        ];
    }
}

