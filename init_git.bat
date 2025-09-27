@echo off
echo ========================================
echo   DataViz Pro - Git Repository Setup
echo ========================================
echo.

echo Initializing Git repository...
git init

echo Adding all files...
git add .

echo Creating initial commit...
git commit -m "Initial commit: DataViz Pro Dashboard with dynamic Git integration"

echo.
echo ========================================
echo   SUCCESS!
echo ========================================
echo Git repository initialized successfully!
echo The "Last Updated" timestamp will now show the actual commit time.
echo.
echo Next steps:
echo 1. Create a GitHub repository
echo 2. Add remote: git remote add origin [your-repo-url]
echo 3. Push: git push -u origin main
echo.
pause
