@echo off
echo ========================================
echo   DataViz Pro Dashboard - GitHub Setup
echo ========================================
echo.

echo Step 1: Initializing Git repository...
git init

echo Step 2: Adding all files...
git add .

echo Step 3: Creating initial commit...
git commit -m "Initial commit: DataViz Pro Dashboard with custom upload functionality"

echo.
echo ========================================
echo   NEXT STEPS:
echo ========================================
echo 1. Go to GitHub.com and create a new repository
echo 2. Name it: dataviz-pro-dashboard
echo 3. Make it PUBLIC for portfolio visibility
echo 4. DON'T initialize with README
echo 5. Copy the repository URL
echo.
echo Then run these commands:
echo git remote add origin https://github.com/YOUR_USERNAME/dataviz-pro-dashboard.git
echo git branch -M main
echo git push -u origin main
echo.
echo ========================================
echo   DEPLOYMENT OPTIONS:
echo ========================================
echo - Heroku: heroku create your-app-name
echo - Railway: Connect via railway.app
echo - Render: Connect via render.com
echo.
echo See DEPLOYMENT_GUIDE.md for detailed instructions
echo.
pause
