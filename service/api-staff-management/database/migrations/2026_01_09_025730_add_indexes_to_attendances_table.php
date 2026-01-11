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
        Schema::table('attendances', function (Blueprint $table) {
            // Composite index for fast daily lookup: user_id + log_date
            // Fast lookup for "did user check in today?" query
            $table->index(['user_id', 'log_date'], 'attendances_user_log_date_index');

            // Index for status filtering (late, on_time, absent)
            //  Fast filtering by status (late, on_time, abse
            $table->index('status','attendances_status_index');

            // Index for log_date (date range queries)
            // Fast date range queries for history
            $table->index('log_date','attendances_log_date_index');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('attendances', function (Blueprint $table) {
            $table->dropIndex('attendances_user_log_date_index');
            $table->dropIndex('attendances_status_index');
            $table->dropIndex('attendances_log_date_index');
        });
    }
};
