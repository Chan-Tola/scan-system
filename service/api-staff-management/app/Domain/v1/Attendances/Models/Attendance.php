<?php

namespace App\Domain\v1\Attendances\Models;

use App\Domain\v1\Offices\Models\Office;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\BelongsTo;
use Illuminate\Database\Eloquent\Relations\HasMany;
use App\Domain\v1\Users\Models\User;

class Attendance extends Model
{
    const TABLENAME = 'attendances';
    protected $table = self::TABLENAME;

    const ID = 'id';
    const USER_ID = 'user_id';
    const LOG_DATE = 'log_date';
    const CHECK_IN = 'check_in';
    const CHECK_OUT = 'check_out';
    const STATUS = 'status';
    const NOTES = 'notes';
    const OFFICE_ID = 'office_id';
    const MINUTES_LATE = 'minutes_late';
    const WORK_HOURS = 'work_hours';

    protected $fillable = [
        self::USER_ID,
        self::LOG_DATE,
        self::CHECK_IN,
        self::CHECK_OUT,
        self::STATUS,
        self::NOTES,
        self::OFFICE_ID,
        self::MINUTES_LATE,
        self::WORK_HOURS,
    ];

    protected $casts = [
        self::LOG_DATE => 'date',
        self::CHECK_IN => 'datetime:H:i:s',
        self::CHECK_OUT => 'datetime:H:i:s',
    ];

    // Relationships
    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function reasons(): HasMany
    {
        return $this->hasMany(AttendanceReason::class);
    }

    // If you add office_id:
    public function office(): BelongsTo
    {
        return $this->belongsTo(Office::class);
    }

}