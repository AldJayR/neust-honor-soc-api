@echo off
echo 🧪 Running Honor Society API tests with pytest...

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
exit /b 1

:python_found
echo 🐍 Using Python command: %PYTHON_CMD%

REM Check what type of test to run
if "%1"=="unit" (
    echo 🎯 Running unit tests only...
    %PYTHON_CMD% -m pytest -v -m unit --ds=honor_system.settings
) else if "%1"=="integration" (
    echo 🔗 Running integration tests only...
    %PYTHON_CMD% -m pytest -v -m integration --ds=honor_system.settings
) else if "%1"=="fast" (
    echo ⚡ Running fast tests (no coverage)...
    %PYTHON_CMD% -m pytest -v --no-cov --ds=honor_system.settings
) else if "%1"=="coverage" (
    echo 📊 Running tests with detailed coverage...
    %PYTHON_CMD% -m pytest --cov=api --cov-report=html --cov-report=term-missing --cov-branch --ds=honor_system.settings
) else (
    echo 🔍 Running all tests with coverage...
    %PYTHON_CMD% -m pytest -v --cov=api --cov-report=term-missing --cov-report=html --ds=honor_system.settings
)

if %errorlevel% == 0 (
    echo ✅ All tests passed!
) else (
    echo ❌ Some tests failed!
    exit /b 1
)

echo.
echo 💡 Usage examples:
echo   test.bat          - Run all tests with coverage
echo   test.bat unit     - Run only unit tests
echo   test.bat integration - Run only integration tests
echo   test.bat fast     - Run tests without coverage
echo   test.bat coverage - Run tests with detailed coverage
