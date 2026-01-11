<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    /**
     * Run the migrations.
     */
    public function up(): void
    {
        Schema::table('attendance_reasons', function (Blueprint $table) {
            // Index for attendance_id (fast lookup of reasons for an attendance)
            $table->index('attendance_id', 'attendance_reasons_attendance_id_index');
            // Index for reason_type (analytics: how many late, early leave)
            $table->index('reason_type', 'attendance_reasons_type_index');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('attendance_reasons', function (Blueprint $table) {
            $table->dropIndex('attendance_reasons_attendance_id_index');
            $table->dropIndex('attendance_reasons_type_index');
        });
    }
};
