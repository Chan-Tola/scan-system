<?php

namespace App\Domain\v1\Attendance_Records\Services;

use App\Domain\v1\Attendances\Models\Attendance;
use Illuminate\Contracts\Pagination\LengthAwarePaginator;
use Illuminate\Support\Facades\DB;

class AttendanceHistoryService
{
    // Get filtered attendances
    public function getFilteredAttendances(
        ?string $name = null,
        ?string $status = null,
        ?string $month = null,
        int $perpage = 15
    ): LengthAwarePaginator {
        $query = Attendance::query()
            ->select([
                'attendances.*',
                DB::raw('(SELECT COUNT(*) FROM attendances a2 WHERE a2.user_id = attendances.user_id AND a2.check_out IS NOT NULL) as stop_count')
            ])->with([
                'user.staff:id,user_id,full_name',
                'reasons:id,attendance_id,reason_type,reason',
                'office:id,name'
            ]);

        // Filter by staff name
        if ($name) {
            $query->whereHas('user.staff', function ($q) use ($name) {
                $q->where('full_name', 'like', "%{$name}%");
            });
        }

        // Filter by Staff name
        if ($status) {
            $query->where('status', $status);
        }

        // Filter by month (YYYY-MM format)
        if ($month) {
            $parts = explode('-', $month);
            if (count($parts) === 2) {
                $year = (int) $parts[0];
                $monthNum = (int) $parts[1];

                $query->whereYear('log_date', $year)
                    ->whereMonth('log_date', $monthNum);
            }
        }

        // Order by most recent first
        $query->orderBy('log_date', 'desc')
            ->orderBy('created_at', 'desc');
        return $query->paginate($perpage);
    }

    // Get statistics
    public function getStatistics(?string $month = null): array
    {
        $query = Attendance::query();

        // Filter by month (YYYY-MM format)
        if ($month) {
            $part = explode('-', $month);
            if (count($part) === 2) {
                $year = (int) $part[0];
                $monthNum = (int) $part[1];

                $query->whereYear('log_date', $year)->whereMonth('log_date', $monthNum);
            }
        } else {
            // Default to currnet month if notspecified
            $query->whereYear('log_date', date('Y'))
                ->whereMonth('log_date', date('m'));
            $month = date('Y-m');
        }

        // Get  count grouped by status
        $statistics = $query->select('status', DB::raw('count(*) as count'))
            ->groupBy('status')
            ->get()
            ->pluck('count', 'status')
            ->toArray();

        return [
            'month' => $month,
            'on_time_count' => $statistics['on_time'] ?? $statistics['present'] ?? 0,
            'late_count' => $statistics['late'] ?? 0,
            'absent_count' => $statistics['absent'] ?? 0,
            'total_records' => array_sum($statistics)
        ];
    }

    public function getUserStopCount(int $userId, ?string $month = null): int
    {
        $query = Attendance::where('user_id', $userId)
            ->whereNotNull('check_out');
        if ($month) {
            $parts = explode('-', $month);
            if (count($parts) === 2) {
                $year = (int) $parts[0];
                $monthNum = (int) $parts[1];

                $query->whereYear('log_date', $year)
                    ->whereMonth('log_date', $monthNum);
            }
        }
        return $query->count();
    }

    // Export query
    public function getExportQuery(
        ?string $name = null,
        ?string $status = null,
        ?string $month = null
    ) {
        $query = Attendance::query()
            ->with([
                'user.staff:id,user_id,full_name',
                'reasons:id,attendance_id,reason_type,reason',
                'office:id,name'
            ]);

        // Apply same filters as getFilteredAttendances
        if ($name) {
            $query->whereHas('user.staff', function ($q) use ($name) {
                $q->where('full_name', 'like', "%{$name}%");
            });
        }
        if ($status) {
            $query->where('status', $status);
        }
        if ($month) {
            $parts = explode('-', $month);
            if (count($parts) === 2) {
                $year = (int) $parts[0];
                $monthNum = (int) $parts[1];

                $query->whereYear('log_date', $year)
                    ->whereMonth('log_date', $monthNum);
            }
        }
        $query->orderBy('log_date', 'desc')
            ->orderBy('created_at', 'desc');
        return $query;
    }
}

