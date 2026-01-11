<?php

namespace App\Domain\v1\Users\Models;

use Illuminate\Database\Eloquent\Factories\HasFactory;
use Illuminate\Database\Eloquent\Relations\HasOne;
// use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Foundation\Auth\User as Authenticatable;
use Illuminate\Notifications\Notifiable;
use Spatie\Permission\Traits\HasRoles;
use App\Domain\v1\Staffs\Models\Staff;
use App\Domain\v1\Attendances\Models\Attendance;
use Illuminate\Database\Eloquent\Relations\HasMany;

class User extends Authenticatable
{
    use HasFactory, Notifiable, HasRoles;

    // ✅ Add this property to specify the guard
    protected $guard_name = 'api';

    const TABLENAME = 'users';
    const ID = 'id';
    const USERNAME = 'username';
    const EMAIL = 'email';
    const PASSWORD =  'password';
    const REMEMBER_TOKEN = 'remember_token';
    const EMAIL_VERIFIED_AT = 'email_verified_at';

    protected $fillable = [
        self::USERNAME,
        self::EMAIL,
        self::PASSWORD,
    ];

    protected $hidden = [
        self::PASSWORD,
        self::REMEMBER_TOKEN,
    ];

    protected function casts(): array
    {
        return [
            self::EMAIL_VERIFIED_AT => 'datetime',
            self::PASSWORD => 'hashed',
        ];
    }

    public function staff(): HasOne
    {
        return $this->hasOne(Staff::class);
    }

    public function attendances(): HasMany
    {
        return $this->hasMany(Attendance::class);
    }
}
