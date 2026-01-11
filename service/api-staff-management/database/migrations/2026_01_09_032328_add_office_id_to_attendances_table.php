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
            // Foreign key to offices (index created automatically)
            $table->foreignId('office_id')->nullable()->after('user_id')->constrained('offices')->onDelete('cascade');
            
            // Column: minutes late (0 if on time)
            $table->integer('minutes_late')->default(0)->after('check_in');
            
            // Column: work hours (decimal for precision)
            $table->decimal('work_hours', 4, 2)->nullable()->after('check_out');
        });
    }

    /**
     * Reverse the migrations.
     */
    public function down(): void
    {
        Schema::table('attendances', function (Blueprint $table) {
            $table->dropForeign(['office_id']);
            $table->dropColumn(['office_id', 'minutes_late', 'work_hours']);
        });
    }
};
