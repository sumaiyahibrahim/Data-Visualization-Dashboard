@echo off
echo ========================================
echo   DataViz Pro - Heroku Deployment
echo ========================================
echo.

echo Step 1: Checking Heroku CLI...
heroku --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Heroku CLI not found!
    echo.
    echo Please install Heroku CLI first:
    echo 1. Go to: https://devcenter.heroku.com/articles/heroku-cli
    echo 2. Download and install Heroku CLI for Windows
    echo 3. Restart your terminal and run this script again
    echo.
    pause
    exit /b 1
)

echo ✅ Heroku CLI found!
echo.

echo Step 2: Login to Heroku...
heroku login

echo Step 3: Creating Heroku app...
set /p APP_NAME=Enter your app name (e.g., my-dataviz-pro): 
heroku create %APP_NAME%

echo Step 4: Setting environment variables...
heroku config:set FLASK_ENV=production --app %APP_NAME%
heroku config:set SECRET_KEY=dataviz-pro-production-key-2024 --app %APP_NAME%

echo Step 5: Adding files to Git...
git add .
git status

echo Step 6: Creating deployment commit...
git commit -m "Deploy: DataViz Pro Dashboard with Git integration to Heroku"

echo Step 7: Deploying to Heroku...
git push heroku main

echo Step 8: Opening your deployed app...
heroku open --app %APP_NAME%

echo.
echo ========================================
echo   🎉 DEPLOYMENT COMPLETE!
echo ========================================
echo.
echo Your DataViz Pro dashboard is now live at:
heroku info --app %APP_NAME% | findstr "Web URL"
echo.
echo Features deployed:
echo ✅ Dynamic Git integration
echo ✅ Real-time commit tracking
echo ✅ Smart filter system
echo ✅ Professional UI/UX
echo ✅ Mobile responsive design
echo ✅ Export functionality
echo.
pause
