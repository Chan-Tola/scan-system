# Git Workflow Notes - Scan System

## 🚀 Initial Setup (Main Branch)
- **Repository:** `https://github.com/Chan-Tola/scan-system.git`
- **Primary Branch:** `main`

git add .
git commit -m "Initial project structure"
git push -u origin main---

## 🌿 Branching Strategy
We use the `feature/` prefix for all new development.

### 1. Priority: Auth & Gateway Security
**Branch:** `feature/auth-system`
- Goal: Setup FastAPI Gateway to read Redis sessions and Spatie tables.
- Goal: Setup Laravel Login to write to Redis.

### 2. Priority: Staff Management
**Branch:** `feature/staff-management`
- Goal: CRUD for Staff, Offices, and QR Code generation.

### 3. Priority: Attendance Logic
**Branch:** `feature/attendance-flow`
- Goal: Check-in/Check-out logic and early leave reasons.

---

## 🛠️ Common Commands

### Creating a new feature branch:
git checkout main
git pull origin main
git checkout -b feature/your-feature-name### Saving progress:
git add .
git commit -m "feat: description of what you did"
git push origin feature/your-feature-name### Merging to Main (When feature is done):
1. Push your branch code.
2. Go to GitHub and create a **Pull Request**.
3. After merging on GitHub, update your local machine:
git checkout main
git pull origin main---

## 📝 Project Architecture Reminders
- **API Gateway:** FastAPI (Port 8000) - Handles Auth & Proxy.
- **Scan Service:** FastAPI - Handles QR logic.
- **Staff Service:** Laravel - Handles DB logic & CRUD.
- **Database:** PostgreSQL (Core data) & Redis (Sessions).