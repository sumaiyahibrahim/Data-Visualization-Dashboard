@echo off
echo ========================================
echo   DataViz Pro Dashboard - Heroku Deploy
echo ========================================
echo.

set /p APP_NAME="Enter your Heroku app name (e.g., my-dataviz-dashboard): "

echo.
echo Step 1: Creating Heroku app...
heroku create %APP_NAME%

echo Step 2: Setting environment variables...
heroku config:set FLASK_ENV=production --app %APP_NAME%
heroku config:set SECRET_KEY=dataviz-pro-secure-key-2024 --app %APP_NAME%

echo Step 3: Deploying to Heroku...
git push heroku main

echo Step 4: Opening your app...
heroku open --app %APP_NAME%

echo.
echo ========================================
echo   DEPLOYMENT COMPLETE!
echo ========================================
echo Your app is now live at:
echo https://%APP_NAME%.herokuapp.com
echo.
echo To update your app in the future:
echo 1. Make changes to your code
echo 2. git add .
echo 3. git commit -m "Update message"
echo 4. git push heroku main
echo.
pause
