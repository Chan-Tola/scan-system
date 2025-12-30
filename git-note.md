# Git Workflow Notes - Scan System

## 🚀 Initial Setup (Main Branch)
- **Repository:** `https://github.com/Chan-Tola/scan-system.git`
- **Primary Branch:** `main`

git add .
git commit -m "Initial project structure"
git push -u origin main---

---

## 🛠️ Common Commands
To create a new feature branch and push it to your GitHub repository

1. Make sure you are on the main branch
git checkout main
git pull origin main

2. Create and switch to the new branch
git checkout -b "name branch"
# example git checkout -b feature/branch

3. (Optional) Push the new branch to GitHub
git push -u origin "name branch"
# example git push -u origin feature/branch

How to work on this branch:

1. Make your changes in the code.

2. Stage and Commit:
git add .
git commit -m "Describe your new feature changes"

3. Push to GitHub:
git push



To safely merge your work into the main branch and update GitHub, follow these steps:

1. Final Save of your Feature
# Ensure you are on your feature branch
git checkout "name branch"
# example git checkout feature/auth-system
# Add and commit any last-minute changes
git add .
git commit -m "write note"
git push origin "name branch"

2. Switch to Main and Update
git checkout main
git pull origin main

3. Merge the Feature into Main
git merge "name branch"

4. Push to GitHub
git push origin main