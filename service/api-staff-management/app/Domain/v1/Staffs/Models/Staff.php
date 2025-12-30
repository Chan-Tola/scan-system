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

    public function user(): BelongsTo
    {
        return $this->belongsTo(User::class);
    }

    public function office(): BelongsTo
    {
        return $this->belongsTo(Office::class);
    }
}
