<?php

namespace App\Domain\v1\Attendance_Records\Exports;

use App\Domain\v1\Attendance_Records\Services\AttendanceHistoryService;
use Maatwebsite\Excel\Concerns\FromQuery;
use Maatwebsite\Excel\Concerns\WithHeadings;
use Maatwebsite\Excel\Concerns\WithMapping;
use Maatwebsite\Excel\Concerns\WithStyles;
use PhpOffice\PhpSpreadsheet\Worksheet\Worksheet;

class AttendanceHistoryExport implements FromQuery, WithHeadings, WithMapping, WithStyles
{
    protected ?string $name;
    protected ?string $status;
    protected ?string $month;
    protected AttendanceHistoryService $service;

    public function __construct(?string $name = null, ?string $status = null, ?string $month = null)
    {
        $this->name = $name;
        $this->status = $status;
        $this->month = $month;
        $this->service = app(AttendanceHistoryService::class);
    }

    /**
     * Get the query for export
     */
    public function query()
    {
        return $this->service->getExportQuery($this->name, $this->status, $this->month);
    }

    /**
     * Define column headings
     */
    public function headings(): array
    {
        return [
            'ID',
            'Staff Name',
            'Username',
            'Email',
            'Office',
            'Date',
            'Check In',
            'Check Out',
            'Status',
            'Minutes Late',
            'Work Hours',
            'Reason Type',
            'Reason',
        ];
    }

    /**
     * Map data for each row
     */
    public function map($attendance): array
    {
        // Get the first reason if exists
        $reason = $attendance->reasons->first();

        return [
            $attendance->id,
            $attendance->user?->staff?->full_name ?? 'N/A',
            $attendance->user?->username ?? 'N/A',
            $attendance->user?->email ?? 'N/A',
            $attendance->office?->name ?? 'N/A',
            $attendance->log_date?->format('Y-m-d') ?? '',
            $attendance->check_in ? date('H:i:s', strtotime($attendance->check_in)) : '',
            $attendance->check_out ? date('H:i:s', strtotime($attendance->check_out)) : '',
            ucfirst(str_replace('_', ' ', $attendance->status)),
            $attendance->minutes_late ?? 0,
            $attendance->work_hours ?? '',
            $reason?->reason_type ?? '',
            $reason?->reason ?? '',
        ];
    }

    /**
     * Apply styles to the worksheet
     */
    public function styles(Worksheet $sheet)
    {
        return [
            // Style the first row (headings)
            1 => [
                'font' => [
                    'bold' => true,
                    'size' => 12,
                ],
                'fill' => [
                    'fillType' => \PhpOffice\PhpSpreadsheet\Style\Fill::FILL_SOLID,
                    'startColor' => ['rgb' => 'E2E8F0'],
                ],
            ],
        ];
    }
}

