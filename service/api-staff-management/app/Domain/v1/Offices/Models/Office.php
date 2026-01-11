<?php

namespace App\Domain\v1\Offices\Models;

use App\Domain\v1\Attendances\Models\Attendance;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use App\Domain\v1\Staffs\Models\Staff;

class Office extends Model
{
    const TABLENAME = 'offices';
    protected $table = self::TABLENAME;

    const ID = 'id';
    const NAME = 'name';
    const PUBLIC_IP = 'public_ip';
    const SHIFT_START = 'shift_start';
    const SHIFT_END = 'shift_end';
    protected $fillable = [
        self::NAME,
        self::PUBLIC_IP,
        self::SHIFT_START,
        self::SHIFT_END,
    ];


    public function staff(): HasMany
    {
        return $this->hasMany(Staff::class);
    }
    public function attendances(): HasMany
    {
        return $this->hasMany(Attendance::class);
    }
}
