<?php

namespace App\Domain\v1\Staffs\Models;

use Illuminate\Database\Eloquent\Model;
use App\Domain\v1\Users\Models\User;
use App\Domain\v1\Offices\Models\Office;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class Staff extends Model
{
    const TABLENAME = 'staff_info';
    protected $table = self::TABLENAME;

    const ID = 'id';
    const USER_ID = 'user_id';
    const OFFICE_ID = 'office_id';
    const FULL_NAME = 'full_name';
    const GENDER = 'gender';
    const PHONE = 'phone';
    const ADDRESS = 'address';
    const DATE_OF_BIRTH = 'date_of_birth';
    const JOIN_DATE = 'join_date';
    const SHIFT_START = 'shift_start';
    const SHIFT_END = 'shift_end';
    const PROFILE_IMAGE = 'profile_image';

    protected $fillable = [
        self::USER_ID,
        self::OFFICE_ID,
        self::FULL_NAME,
        self::GENDER,
        self::PHONE,
        self::ADDRESS,
        self::DATE_OF_BIRTH,
        self::JOIN_DATE,
        self::SHIFT_START,
        self::SHIFT_END,
        self::PROFILE_IMAGE,
    ];

    protected static function boot()
    {
        parent::boot();

        static::creating(function ($staff) {
            //  If shift time are not provided, set it to the office shift time
            if (empty($staff->shift_start) || empty($staff->shift_end)) {
                $office = Office::find($staff->office_id);
                if ($office && $office->shift_start && $office->shift_end) {
                    $staff->shift_start = $staff->shift_start ?? $office->shift_start;
                    $staff->shift_end = $staff->shift_end ?? $office->shift_end;
                }
            }
        });

        // Update shift time when office location changes
        static::updating(function ($staff) {
            // Check if office_id is being changed
            if ($staff->isDirty('office_id')) {
                // Get the new office
                $newOffice = Office::find($staff->office_id);

                // Update shift times to match new office schedule
                if ($newOffice && $newOffice->shift_start && $newOffice->shift_end) {
                    $staff->shift_start = $newOffice->shift_start;
                    $staff->shift_end = $newOffice->shift_end;
                }
            }
        });
    }

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function office(): BelongsTo
    {
        return $this->belongsTo(Office::class);
    }

    /**
     * Get optimized profile image URL with transformations applied on-demand
     * This accessor automatically optimizes the image URL when accessed
     */
    public function getProfileImageOptimizedAttribute(): ?string
    {
        if (!$this->profile_image) {
            return null;
        }

        // Use StaffService to get optimized URL
        $staffService = app(\App\Domain\v1\Staffs\Services\StaffService::class);
        return $staffService->getOptimizedImageUrl($this->profile_image);
    }
}
