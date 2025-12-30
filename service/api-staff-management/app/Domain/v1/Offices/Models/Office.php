<?php

namespace App\Domain\v1\Offices\Models;

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

    protected $fillable = [
        self::NAME,
        self::PUBLIC_IP,
    ];

    
    public function staff(): HasMany
    {
        return $this->hasMany(Staff::class);
    }
}

