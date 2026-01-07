<?php

namespace App\Domain\v1\Staffs\Resources;

use Illuminate\Http\Resources\Json\JsonResource;

class StaffResource extends JsonResource
{
    public function toArray($request)
    {
        return [
            'id'            => $this->id,
            'username'      => $this->user->username ?? null,
            'full_name'     => $this->full_name,
            'phone'         => $this->phone,
            'email'         => $this->user->email ?? null,
            'role'          => $this->user->roles->first()->name ?? 'staff',
            'office_name'   => $this->office->name ?? 'N/A',
            // Formatting: 08:00:00 -> 08:00
            'shift'         => ($this->shift_start && $this->shift_end)
                ? substr($this->shift_start, 0, 5) . ' - ' . substr($this->shift_end, 0, 5)
                : 'N/A',
            'join_date'     => $this->join_date,
            'profile_image' => $this->profile_image_optimized ?? $this->profile_image,
        ];
    }
}
