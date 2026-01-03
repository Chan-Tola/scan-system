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
        Schema::table('staff_info', function (Blueprint $table) {
            // Foreign keys should always be indexed
            $table->index('user_id');
            $table->index('office_id');

            // // Search columns
            $table->index('full_name');
            $table->index('phone');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('staff_info', function (Blueprint $table) {
            //
        });
    }
};
