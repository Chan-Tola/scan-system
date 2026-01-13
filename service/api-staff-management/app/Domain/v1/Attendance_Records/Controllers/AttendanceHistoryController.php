<?php

namespace App\Domain\v1\Attendance_Records\Controllers;

use App\Http\Controllers\Controller;
use Illuminate\Http\JsonResponse;
use Illuminate\Http\Request;
use App\Domain\v1\Attendance_Records\Requests\AttendanceHistoryRequest;
use App\Domain\v1\Attendance_Records\Resources\AttendanceHistoryResource;
use App\Domain\v1\Attendance_Records\Resources\MonthlyStatisticsResource;
use App\Domain\v1\Attendance_Records\Services\AttendanceHistoryService;
use App\Domain\v1\Attendance_Records\Exports\AttendanceHistoryExport;
use Maatwebsite\Excel\Facades\Excel;


class AttendanceHistoryController extends Controller
{

    protected AttendanceHistoryService $historyService;
    public function __construct(AttendanceHistoryService $historyService)
    {
        $this->historyService = $historyService;
    }


    // Get paginated attendance history with filters
    public function index(AttendanceHistoryRequest $request): JsonResponse
    {
        try {
            $validated = $request->validated();

            // Get filtered and paginated attendances
            $attendances = $this->historyService->getFilteredAttendances(
                name: $validated['name'] ?? null,
                status: $validated['status'] ?? null,
                month: $validated['month'] ?? null,
                perpage: $validated['per_page']
            );
            return response()->json([
                'status' => 'success',
                'data' => AttendanceHistoryResource::collection($attendances->items()),
                'pagination' => [
                    'current_page' => $attendances->currentPage(),
                    'total' => $attendances->total(),
                    'last_page' => $attendances->lastPage(),
                    'per_page' => $attendances->perPage(),
                ]
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to fetch attendance history: ' . $e->getMessage()
            ], 500);
        }
    }

    //  Get monthly statistics (count of on_time, late, absent)
    public function statistics(Request $request): JsonResponse
    {
        try {
            $month = $request->query('month'); // Optional: YYYY-MM format

            $statistics = $this->historyService->getStatistics($month);
            return response()->json([
                'status' => 'success',
                'data' => new MonthlyStatisticsResource($statistics)
            ]);
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to fetch statistics: ' . $e->getMessage()
            ], 500);
        }
    }


    // Export attendance history to Excel
    public function export(AttendanceHistoryRequest $request)
    {
        try {
            $validated = $request->validated();

            // Generate filename with timestamp
            $filename = 'attendance_history_' . date('Y-m-d_His') . '.xlsx';

            return Excel::download(
                new AttendanceHistoryExport(
                    name: $validated['name'] ?? null,
                    status: $validated['status'] ?? null,
                    month: $validated['month'] ?? null
                ),
                $filename
            );
        } catch (\Exception $e) {
            return response()->json([
                'status' => 'error',
                'message' => 'Failed to export: ' . $e->getMessage()
            ], 500);
        }
    }
}

