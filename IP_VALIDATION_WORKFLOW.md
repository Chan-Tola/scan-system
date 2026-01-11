# IP Validation Workflow

## Complete System Flow

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        USER SCANS QR CODE                                │
│                  (Home IP: 58.97.212.120)                                │
└────────────────────────────┬────────────────────────────────────────────┘
                             │
                             ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                      FRONTEND (Browser)                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 1. QR Scanner captures QR code token                             │  │
│  │    Example: "WeYxpr9hN4Vd284raMrQz1Ie06rtlHTq"                   │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
│                               │                                          │
│                               ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 2. Get User's Public IP                                           │  │
│  │    File: getPublicIp.ts                                           │  │
│  │    API: https://api.ipify.org?format=json                        │  │
│  │    Response: { "ip": "58.97.212.120" }                          │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
│                               │                                          │
│                               ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 3. Prepare Request                                                │  │
│  │    File: attendanceApi.ts                                         │  │
│  │    Request Body:                                                  │  │
│  │    {                                                              │  │
│  │      "qr_token": "WeYxpr9hN4Vd284raMrQz1Ie06rtlHTq",            │  │
│  │      "client_ip": "58.97.212.120"  ← Client-provided IP         │  │
│  │    }                                                              │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────────┘
                                │
                                │ POST /api/scan/validate-qr
                                │ (with client_ip in body)
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                     API GATEWAY                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 4. Route to API-Scan Service                                      │  │
│  │    Forward request to: http://api-scan:8001/scan/validate-qr     │  │
│  │    Headers: X-User-ID, X-Forwarded-For, etc.                     │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    API-SCAN SERVICE                                      │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 5. Route Handler                                                  │  │
│  │    File: route_attendance.py                                     │  │
│  │    Function: validate_qr_code()                                  │  │
│  │                                                                   │  │
│  │    Priority Check:                                                │  │
│  │    IF request.client_ip exists (from body):                      │  │
│  │      ✅ Use client-provided IP: "58.97.212.120"                  │  │
│  │      Print: "Using client-provided IP: 58.97.212.120"           │  │
│  │    ELSE:                                                          │  │
│  │      → Extract from headers (X-Real-IP, X-Forwarded-For)         │  │
│  │      → Fallback to request.client.host                           │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
│                               │                                          │
│                               ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 6. Service Layer - Validation                                     │  │
│  │    File: attendance_controller.py                                │  │
│  │    Function: validate_qr_code()                                  │  │
│  │                                                                   │  │
│  │    Steps:                                                         │  │
│  │    a) Find QR code by token                                      │  │
│  │    b) Get office information                                     │  │
│  │    c) Check if office has public_ip configured                   │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
│                               │                                          │
│                               ▼                                          │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ 7. IP Validation Logic                                            │  │
│  │                                                                   │  │
│  │    IF office.public_ip exists:                                   │  │
│  │      │                                                            │  │
│  │      ├─ Check if client_ip exists:                               │  │
│  │      │   IF NOT: ❌ Reject (No IP provided)                      │  │
│  │      │                                                            │  │
│  │      ├─ Check if IP is Docker/internal (172.x, 10.x, 192.168.x):│  │
│  │      │   IF YES: ❌ Reject (Should use public IP)                │  │
│  │      │                                                            │  │
│  │      ├─ Compare client_ip with office.public_ip:                 │  │
│  │      │                                                            │  │
│  │      │   Example:                                                │  │
│  │      │   ┌────────────────────────────────────┐                  │  │
│  │      │   │ client_ip: "58.97.212.120"        │                  │  │
│  │      │   │ office.public_ip: "58.97.212.120" │                  │  │
│  │      │   │ Result: ✅ MATCH → VALIDATE        │                  │  │
│  │      │   └────────────────────────────────────┘                  │  │
│  │      │                                                            │  │
│  │      │   ┌────────────────────────────────────┐                  │  │
│  │      │   │ client_ip: "58.97.212.120"        │                  │  │
│  │      │   │ office.public_ip: "111.90.182.177"│                  │  │
│  │      │   │ Result: ❌ MISMATCH → REJECT       │                  │  │
│  │      │   └────────────────────────────────────┘                  │  │
│  │      │                                                            │  │
│  │      └─ IF MATCH: ✅ Return valid response                       │  │
│  │         ELSE: ❌ Return invalid response                         │  │
│  └────────────────────────────┬──────────────────────────────────────┘  │
└───────────────────────────────┼──────────────────────────────────────────┘
                                │
                                │ Response
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    RESPONSE TO FRONTEND                                  │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ IF VALID:                                                         │  │
│  │ {                                                                 │  │
│  │   "valid": true,                                                 │  │
│  │   "message": "QR code is valid",                                 │  │
│  │   "office": {                                                    │  │
│  │     "id": 38,                                                    │  │
│  │     "name": "Home",                                              │  │
│  │     "public_ip": "58.97.212.120"                                │  │
│  │   }                                                               │  │
│  │ }                                                                 │  │
│  │                                                                   │  │
│  │ IF INVALID:                                                       │  │
│  │ {                                                                 │  │
│  │   "valid": false,                                                │  │
│  │   "message": "IP address mismatch. You must be at Office...",   │  │
│  │   "office": null                                                 │  │
│  │ }                                                                 │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────────────────┐
│                    FRONTEND DISPLAYS RESULT                              │
│  ┌───────────────────────────────────────────────────────────────────┐  │
│  │ IF VALID:                                                         │  │
│  │   → Show success toast: "QR Code Valid - Office: Home"           │  │
│  │   → Enable check-in button                                        │  │
│  │                                                                   │  │
│  │ IF INVALID:                                                       │  │
│  │   → Show error toast: "IP address mismatch..."                   │  │
│  │   → Disable check-in button                                       │  │
│  └───────────────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────────────┘
```

## Key Components

### 1. **Frontend (Browser)**
- **Location**: `scan-system-dashboard/src/features/scan/`
- **Files**:
  - `utils/getPublicIp.ts` - Gets user's public IP
  - `services/attendanceApi.ts` - Sends request with client IP
  - `store/attendanceStore.ts` - Handles validation state

### 2. **API Gateway**
- **Location**: `api-gateway/app/`
- **Role**: Routes requests to appropriate service
- **Forwards**: Headers (X-User-ID, X-Forwarded-For, etc.)

### 3. **API-Scan Service (Backend)**
- **Location**: `service/api-scan/app/Domain/v1/Attendances/`
- **Files**:
  - `Routes/route_attendance.py` - HTTP route handlers
  - `Controllers/attendance_controller.py` - Business logic
  - `Schemas/attendance_schema.py` - Request/response models

## IP Priority Logic

```
Priority Order:
┌─────────────────────────────────────────────────────────┐
│ 1. Client-provided IP (from request body)               │ ← HIGHEST PRIORITY
│    - Fetched by frontend using ipify.org                │
│    - Sent in request body as "client_ip"                │
│    - Works even when accessing through local network    │
│                                                          │
│ 2. X-Real-IP header (from nginx)                        │
│    - Set by nginx reverse proxy                         │
│    - Most reliable when accessing via public internet   │
│                                                          │
│ 3. X-Forwarded-For header (leftmost IP)                 │
│    - Proxy chain header                                 │
│    - Leftmost IP is original client                     │
│                                                          │
│ 4. request.client.host (direct connection)              │ ← FALLBACK
│    - Direct connection IP                               │
│    - Usually Docker IP when in local network            │
└─────────────────────────────────────────────────────────┘
```

## Example Scenarios

### Scenario 1: User at Home Validates Home QR Code ✅
```
User Location: Home
User Public IP: 58.97.212.120
Office Public IP: 58.97.212.120 (Home)

Flow:
1. Frontend gets IP: 58.97.212.120
2. Sends to backend: { qr_token: "...", client_ip: "58.97.212.120" }
3. Backend compares: 58.97.212.120 == 58.97.212.120
4. Result: ✅ VALID → Can validate
```

### Scenario 2: User at Home Validates Office QR Code ❌
```
User Location: Home
User Public IP: 58.97.212.120
Office Public IP: 111.90.182.177 (Office)

Flow:
1. Frontend gets IP: 58.97.212.120
2. Sends to backend: { qr_token: "...", client_ip: "58.97.212.120" }
3. Backend compares: 58.97.212.120 != 111.90.182.177
4. Result: ❌ INVALID → Rejected
```

### Scenario 3: User at Office Validates Office QR Code ✅
```
User Location: Office
User Public IP: 111.90.182.177
Office Public IP: 111.90.182.177 (Office)

Flow:
1. Frontend gets IP: 111.90.182.177
2. Sends to backend: { qr_token: "...", client_ip: "111.90.182.177" }
3. Backend compares: 111.90.182.177 == 111.90.182.177
4. Result: ✅ VALID → Can validate
```

## Security Features

1. **Client-side IP detection**: Uses external API (ipify.org) to get real public IP
2. **Server-side validation**: Backend validates IP against office public IP in database
3. **Strict matching**: IP must exactly match office public IP
4. **Docker IP rejection**: Rejects internal/Docker IPs to ensure public IP is used
5. **Location-based access**: Users can only validate QR codes for their current location

## Benefits

✅ Works even when accessing through local network (192.168.x.x)  
✅ No need to configure router/port forwarding  
✅ Real-time IP detection using external API  
✅ Secure validation on server side  
✅ Clear error messages for users  

