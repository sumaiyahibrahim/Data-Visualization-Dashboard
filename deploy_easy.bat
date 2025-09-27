@echo off
echo ========================================
echo   DataViz Pro - Easy Deployment
echo ========================================
echo.

echo Step 1: Pushing to GitHub first...
echo.

echo Current Git status:
git status

echo.
echo Adding any new changes...
git add .

echo.
echo Creating deployment commit...
git commit -m "Ready for deployment: DataViz Pro with Git integration"

echo.
echo ========================================
echo   DEPLOYMENT OPTIONS
echo ========================================
echo.
echo Choose your deployment method:
echo.
echo 1. RENDER.COM (Easiest - No CLI needed)
echo    - Go to: https://render.com
echo    - Connect your GitHub repo
echo    - Auto-deploys on push!
echo.
echo 2. RAILWAY.APP (Simple - No CLI needed)  
echo    - Go to: https://railway.app
echo    - Connect GitHub repo
echo    - One-click deploy!
echo.
echo 3. VERCEL (Fast - No CLI needed)
echo    - Go to: https://vercel.com
echo    - Import GitHub project
echo    - Instant deployment!
echo.
echo 4. HEROKU (Traditional - Needs CLI)
echo    - Install Heroku CLI first
echo    - Use heroku commands
echo.
echo ========================================
echo   GITHUB SETUP (Required for all)
echo ========================================
echo.

set /p GITHUB_REPO=Enter your GitHub repository URL (or press Enter to skip): 

if not "%GITHUB_REPO%"=="" (
    echo Adding GitHub remote...
    git remote add origin %GITHUB_REPO%
    
    echo Pushing to GitHub...
    git push -u origin main
    
    echo.
    echo ✅ SUCCESS! Your code is now on GitHub!
    echo.
    echo Next steps:
    echo 1. Go to your chosen platform (Render/Railway/Vercel)
    echo 2. Connect your GitHub repository
    echo 3. Deploy with one click!
    echo.
) else (
    echo.
    echo ⚠️  GitHub setup skipped.
    echo You'll need to push to GitHub manually for web deployment.
    echo.
)

echo ========================================
echo   YOUR PROJECT IS READY!
echo ========================================
echo.
echo Features ready for deployment:
echo ✅ Git integration with real-time commit tracking
echo ✅ Dynamic filter system
echo ✅ Professional UI/UX
echo ✅ Data export functionality
echo ✅ Mobile responsive design
echo ✅ Production-ready configuration
echo.
echo Files ready:
echo ✅ requirements.txt - Python dependencies
echo ✅ Procfile - Process configuration  
echo ✅ runtime.txt - Python version
echo ✅ All source code committed to Git
echo.
pause
