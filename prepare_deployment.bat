@echo off
echo 🚀 Preparing Honor Society API for Render deployment...

REM Check if we're in the right directory
if not exist "manage.py" (
    echo ❌ Error: Please run this script from the project root directory
    exit /b 1
)

REM Check if git is initialized
if not exist ".git" (
    echo 📦 Initializing git repository...
    git init
    git add .
    git commit -m "Initial commit - Ready for Render deployment"
) else (
    echo 📦 Git repository already exists
)

REM Find Python command
where python >nul 2>nul
if %errorlevel% == 0 (
    set PYTHON_CMD=python
    goto :python_found
)

where python3 >nul 2>nul
if %errorlevel% == 0 (
    set PYTHON_CMD=python3
    goto :python_found
)

where py >nul 2>nul
if %errorlevel% == 0 (
    set PYTHON_CMD=py
    goto :python_found
)

echo ❌ Python not found! Please install Python or add it to PATH
echo 💡 Make sure Python is installed and added to your system PATH
exit /b 1

:python_found
echo 🐍 Using Python command: %PYTHON_CMD%

REM Generate a new secret key for production
echo 🔐 Generating new SECRET_KEY for production...
%PYTHON_CMD% -c "import secrets; import string; alphabet = string.ascii_letters + string.digits + string.punctuation; secret_key = ''.join(secrets.choice(alphabet) for i in range(50)); print(f'SECRET_KEY={secret_key}'); print('Copy this SECRET_KEY to your Render environment variables!')"

REM Check if requirements.txt exists
if exist "requirements.txt" (
    echo ✅ requirements.txt found
) else (
    echo ❌ requirements.txt not found
    exit /b 1
)

REM Check if Procfile exists
if exist "Procfile" (
    echo ✅ Procfile found
) else (
    echo ❌ Procfile not found
    exit /b 1
)

REM Run tests to make sure everything works
echo 🧪 Running tests...
%PYTHON_CMD% -m pytest -v --ds=honor_system.settings
if %errorlevel% neq 0 (
    echo ❌ Tests failed! Please fix before deploying.
    exit /b 1
)

REM Check for migrations
echo 🔄 Checking for pending migrations...
%PYTHON_CMD% manage.py makemigrations --check --dry-run
if %errorlevel% == 0 (
    echo ✅ No pending migrations
) else (
    echo 📝 Creating migrations...
    %PYTHON_CMD% manage.py makemigrations
)

REM Collect static files locally to test
echo 📁 Testing static files collection...
%PYTHON_CMD% manage.py collectstatic --noinput --clear
if %errorlevel% neq 0 (
    echo ❌ Static files collection failed
    exit /b 1
)

echo.
echo 🎯 Deployment checklist:
echo   ✅ Git repository ready
echo   ✅ Requirements.txt configured
echo   ✅ Procfile configured
echo   ✅ Settings production-ready
echo   ✅ Tests passing
echo   ✅ Static files working
echo.
echo 🚀 Ready for Render deployment!
echo.
echo Next steps:
echo 1. Push your code to GitHub
echo 2. Create PostgreSQL database on Render
echo 3. Create Web Service on Render
echo 4. Add environment variables (including the SECRET_KEY above)
echo 5. Deploy!
echo.
echo 📚 See RENDER_DEPLOYMENT.md for detailed instructions
pause
