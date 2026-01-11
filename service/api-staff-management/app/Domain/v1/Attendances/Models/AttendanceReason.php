<?php

namespace App\Domain\v1\Attendances\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;

class AttendanceReason extends Model
{
    const TABLENAME = 'attendance_reasons';
    protected $table = self::TABLENAME;

    // Column constants
    const ID = 'id';
    const ATTENDANCE_ID = 'attendance_id';
    const REASON_TYPE = 'reason_type';
    const REASON = 'reason';

    protected $fillable = [
        self::ATTENDANCE_ID,
        self::REASON_TYPE,
        self::REASON,
    ];

    // Relationships
    public function attendance(): BelongsTo
    {
        return $this->belongsTo(Attendance::class);
    }
}