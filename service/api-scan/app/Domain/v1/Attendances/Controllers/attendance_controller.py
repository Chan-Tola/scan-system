from sqlalchemy.orm import Session 
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime, date, time as dt_time, timezone

from app.Domain.v1.Attendances.Models.attendance_model import Attendance
from app.Domain.v1.Attendances.Models.attendance_reason_model import AttendanceReason
from app.Domain.v1.QR_codes.Models.qr_model import QRCode
from app.Domain.v1.Offices.Models.office_model import Office

from app.Domain.v1.Attendances.Schemas.attendance_schema import (
    CheckInRequest,
    CheckInResponse,
    CheckOutRequest,
    CheckOutResponse,
    AttendanceResponse,
    QRValidationRequest,
    QRValidationResponse,
    OfficeInfo    
)

class AttendanceService:
    """ Service layer for attendance bussiness logic """
    # Help Methods

    @staticmethod
    def _get_qr_code_or_404(db: Session, qr_token: str) -> QRCode:
        """  Get QR code by token or raise 404 """
        qr_code = db.query(QRCode).filter(QRCode.qr_token == qr_token).first()
        if not qr_code:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"QR code with token '{qr_token}' not found")
        return qr_code

    @staticmethod
    def _get_office_or_404(db: Session, office_id: int) -> Office:
        """Get office by ID or raise 404"""
        office = db.query(Office).filter(Office.id == office_id).first()
        if not office:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Office {office_id} not found"
            )
        return office
    @staticmethod
    def _calculate_minutes_late(check_in: dt_time, shift_start: dt_time) -> int:
        """Calculate how many minutes late the user is"""
        # convert time to minutes since midnight
        check_in_minutes = check_in.hour * 60 + check_in.minute
        shift_start_minutes = shift_start.hour * 60 + shift_start.minute

        # Calculate difference
        late_minutes = check_in_minutes - shift_start_minutes
        return max(0, late_minutes)
    
    @staticmethod
    def _determine_status(minutes_late: int) -> str:
        """Determine attendance status based on minutes late"""
        if minutes_late == 0:
            return "present"
        else:
            return "late"
    
    @staticmethod
    def validate_qr_code(db: Session, request: QRValidationRequest) -> QRValidationResponse:
        """ Validate QR code and return office info """
        try:
            qr_code = AttendanceService._get_qr_code_or_404(db, request.qr_token)

            # Check if QR code is active
            if not qr_code.is_active:
                return QRValidationResponse(
                    valid=False,
                    message="QR code is inactive",
                    office=None
                )
            
            # Get office information
            office = AttendanceService._get_office_or_404(db, qr_code.office_id)

            # SECURITY: Validate client IP matches office IP (STRICT MODE)
            # This prevents staff from validating QR codes remotely
            if office.public_ip:
                print(f"DEBUG: Office {office.name} has public_ip: {office.public_ip}")
                print(f"DEBUG: Client IP extracted: {request.client_ip}")
                
                # ALWAYS require client_ip when office.public_ip is configured
                if not request.client_ip:
                    print(f"DEBUG: Validation FAILED - No client IP extracted")
                    return QRValidationResponse(
                        valid=False,
                        message="Unable to determine your IP address. Validation requires IP verification. Please ensure you are connected to the network.",
                        office=None
                    )
                
                # STRICT VALIDATION: Always require IP match when office.public_ip is set
                # Use client-provided IP (from frontend) if available, otherwise use server-extracted IP
                # This allows validation to work even when accessing through local network
                is_docker_ip = request.client_ip.startswith(("172.", "10.", "192.168.", "127."))
                print(f"DEBUG: Is Docker/internal IP: {is_docker_ip}")
                
                if is_docker_ip:
                    # Docker/internal IP detected - this means server couldn't extract public IP
                    # Client should provide their public IP in the request body
                    # If we still see Docker IP, validation fails (client didn't provide public IP)
                    print(f"DEBUG: Validation FAILED - Docker/internal IP detected: {request.client_ip}. Client should provide public IP in request. Expected Office IP: {office.public_ip}")
                    return QRValidationResponse(
                        valid=False,
                        message=f"Unable to validate IP address. Server detected internal network IP ({request.client_ip}) instead of your public IP. Expected Office IP: {office.public_ip}",
                        office=None
                    )
                
                # Public IP detected (either from client or server) - strict comparison required
                if request.client_ip != office.public_ip:
                    print(f"DEBUG: Validation FAILED - IP mismatch: {request.client_ip} != {office.public_ip}")
                    return QRValidationResponse(
                        valid=False,
                        message=f"IP address mismatch. You must be at {office.name} to validate this QR code. Your IP: {request.client_ip}, Expected Office IP: {office.public_ip}",
                        office=None
                    )
                else:
                    print(f"DEBUG: Validation PASSED - IP matches: {request.client_ip} == {office.public_ip}")

            return QRValidationResponse(
                valid=True,
                message="QR code is valid",
                office=OfficeInfo(
                    id=office.id,
                    name=office.name,
                    public_ip=office.public_ip
                )
            )
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to validate QR code: {str(e)}")

    @staticmethod
    def check_in(db: Session, user_id: int, request: CheckInRequest, client_ip: Optional[str] = None) -> CheckInResponse:
        """ Handle user check-in with IP validation """
        try:
            # 1. Validate QR Code
            qr_code = AttendanceService._get_qr_code_or_404(db, request.qr_token)

            if not qr_code.is_active:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="QR code is inactive")

            # 2. Get office information
            office = AttendanceService._get_office_or_404(db, qr_code.office_id)

            # 2.5. SECURITY: Validate client IP matches office IP (STRICT MODE)
            # This prevents staff from checking in remotely using screenshots of QR codes
            if office.public_ip:
                print(f"DEBUG: Office {office.name} has public_ip: {office.public_ip}")
                print(f"DEBUG: Client IP extracted: {client_ip}")
                
                # ALWAYS require client_ip when office.public_ip is configured
                if not client_ip:
                    print(f"DEBUG: Check-in FAILED - No client IP extracted")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="Unable to determine your IP address. Check-in requires IP validation. Please ensure you are connected to the network."
                    )

                # STRICT VALIDATION: Always require IP match when office.public_ip is set
                # Use client-provided IP (from frontend) if available, otherwise use server-extracted IP
                # This allows validation to work even when accessing through local network
                is_docker_ip = client_ip.startswith(("172.", "10.", "192.168.", "127.", "localhost"))
                print(f"DEBUG: Is Docker/internal IP: {is_docker_ip}")

                if is_docker_ip:
                    # Docker/internal IP detected - this means server couldn't extract public IP
                    # Client should provide their public IP in the request body
                    # If we still see Docker IP, validation fails (client didn't provide public IP)
                    print(f"DEBUG: Check-in FAILED - Docker/internal IP detected: {client_ip}. Client should provide public IP in request. Expected Office IP: {office.public_ip}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"Unable to validate IP address. Server detected internal network IP ({client_ip}) instead of your public IP. Expected Office IP: {office.public_ip}"
                    )
                
                # Public IP detected (either from client or server) - strict comparison required
                if client_ip != office.public_ip:
                    print(f"DEBUG: Check-in FAILED - IP mismatch: {client_ip} != {office.public_ip}")
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"IP address mismatch. You must be at {office.name} to check in. Your IP: {client_ip}, Expected Office IP: {office.public_ip}"
                    )
                else:
                    print(f"DEBUG: Check-in PASSED - IP matches: {client_ip} == {office.public_ip}")

            # 3. Check if user already checked in today
            today = date.today()
            existing_attendance = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.log_date == today
            ).first()

            if existing_attendance:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="You have already checked in today"
                )
            
            # 4. Get current time and calculate if late
            # Use Asia/Bangkok timezone (UTC+7) instead of UTC
            from zoneinfo import ZoneInfo
            bangkok_tz = ZoneInfo("Asia/Bangkok")
            now = datetime.now(bangkok_tz)
            check_in_time = now.time()

            minute_late = AttendanceService._calculate_minutes_late(
                check_in_time,
                office.shift_start
            )

            attendance_status = AttendanceService._determine_status(minute_late)

            # 5 Create attendance recoard
            attendance = Attendance(
                user_id =user_id,
                office_id = office.id,
                log_date = today,
                check_in = check_in_time,
                status = attendance_status,
                minutes_late = minute_late,
                created_at=now,
                updated_at=now
            )

            db.add(attendance)
            db.commit()
            db.refresh(attendance)

            # 6. Format response
            return CheckInResponse(
                message="Check-in successful" if minute_late == 0 else f"Checked in {minute_late} minutes late",
                attendance=AttendanceResponse(
                    id=attendance.id,
                    user_id=attendance.user_id,
                    office_id=attendance.office_id,
                    log_date=attendance.log_date,
                    check_in=attendance.check_in,
                    check_out=attendance.check_out,
                    status=attendance.status,
                    minutes_late=attendance.minutes_late,
                    work_hours=attendance.work_hours,
                    created_at=attendance.created_at,
                    updated_at=attendance.updated_at,
                    office=OfficeInfo(
                        id=office.id,
                        name=office.name,
                        public_ip=office.public_ip
                    ),
                    attendance_reasons=[]
                ),
                is_late=minute_late > 0,
                minutes_late=minute_late
            )

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to check in: {str(e)}"
                )
    
    @staticmethod
    def check_out(db: Session, user_id: int, request: CheckOutRequest) -> CheckOutResponse:
        """ Handle user check-out with early leave detection """
        try:
            # 1. Get today's attendance
            today = date.today()
            attendance = db.query(Attendance).filter(
                Attendance.user_id == user_id,
                Attendance.log_date == today
            ).first()

            if not attendance:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No check-in record found for today. Please check in first."
                )

            # 2. Check if already checked out
            if attendance.check_out:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"You have already checked out at {attendance.check_out.strftime('%H:%M:%S')}"
                )

            # 3. Get office information
            office = AttendanceService._get_office_or_404(db, attendance.office_id)

            # 4. Get current time
            from zoneinfo import ZoneInfo
            bangkok_tz = ZoneInfo("Asia/Bangkok")
            now = datetime.now(bangkok_tz)
            check_out_time = now.time()

            # 5. Calculate work hours
            check_in_datetime = datetime.combine(today, attendance.check_in)
            check_out_datetime = datetime.combine(today, check_out_time)
            work_duration = check_out_datetime - check_in_datetime
            work_hours = round(work_duration.total_seconds() / 3600, 2)  # Convert to hours

            # 6. Determine if early leave
            check_out_minutes = check_out_time.hour * 60 + check_out_time.minute
            shift_end_minutes = office.shift_end.hour * 60 + office.shift_end.minute
            is_early_leave = check_out_minutes < shift_end_minutes

            # 7. Update attendance record
            attendance.check_out = check_out_time
            attendance.work_hours = work_hours
            attendance.updated_at = now

            # 8. Create reason record if provided (for audit trail)
            # Save reason regardless of early leave status for complete audit history
            if request.reason:
                reason_record = AttendanceReason(
                    attendance_id=attendance.id,
                    reason_type="early_leave" if is_early_leave else "check_out_note",
                    reason=request.reason,
                    created_at=now,
                    updated_at=now
                )
                db.add(reason_record)

            db.commit()
            db.refresh(attendance)

            # 9. Format response
            return CheckOutResponse(
                message="Check-out successful" if not is_early_leave else f"Early check-out recorded. Work hours: {work_hours}",
                attendance=AttendanceResponse(
                    id=attendance.id,
                    user_id=attendance.user_id,
                    office_id=attendance.office_id,
                    log_date=attendance.log_date,
                    check_in=attendance.check_in,
                    check_out=attendance.check_out,
                    status=attendance.status,
                    minutes_late=attendance.minutes_late,
                    work_hours=attendance.work_hours,
                    created_at=attendance.created_at,
                    updated_at=attendance.updated_at,
                    office=OfficeInfo(
                        id=office.id,
                        name=office.name,
                        public_ip=office.public_ip
                    ),
                    attendance_reasons=[]
                ),
                work_hours=work_hours,
                is_early_leave=is_early_leave
            )

        except HTTPException:
            raise
        except Exception as e:
            db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to check out: {str(e)}"
            )
