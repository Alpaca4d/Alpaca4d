@echo off
setlocal enabledelayedexpansion

REM Alpaca4d Plugin Publishing Script for McNeel Package Manager (Windows)
REM This script builds the project, copies files to YAK directory, and publishes to Package Manager

REM Configuration
set "PROJECT_ROOT=%~dp0.."
set "YAK_DIR=%PROJECT_ROOT%\YAK"
set "MANIFEST_FILE=%YAK_DIR%\manifest.yml"
set "TOKEN_FILE=%USERPROFILE%\.mcneel\yak.yml"

REM Colors for output (Windows 10+)
set "BLUE=[94m"
set "GREEN=[92m"
set "YELLOW=[93m"
set "RED=[91m"
set "NC=[0m"

REM Function to print colored output
:print_status
echo %BLUE%[INFO]%NC% %~1
goto :eof

:print_success
echo %GREEN%[SUCCESS]%NC% %~1
goto :eof

:print_warning
echo %YELLOW%[WARNING]%NC% %~1
goto :eof

:print_error
echo %RED%[ERROR]%NC% %~1
goto :eof

REM Function to check if yak is available
:check_yak
yak --version >nul 2>&1
if errorlevel 1 (
    call :print_error "Yak command not found. Please install yak CLI tool."
    call :print_status "Download from: https://developer.rhino3d.com/guides/yak/yak-cli-reference/"
    exit /b 1
)
call :print_success "Yak CLI found"
goto :eof

REM Function to check authentication
:check_auth
if not exist "%TOKEN_FILE%" (
    call :print_error "Authentication token not found at %TOKEN_FILE%"
    call :print_status "Please run 'yak login' first to authenticate"
    exit /b 1
)
call :print_success "Authentication token found"
goto :eof

REM Function to get current version from manifest
:get_current_version
for /f "tokens=2" %%i in ('findstr "^version:" "%MANIFEST_FILE%"') do set "current_version=%%i"
goto :eof

REM Function to update version in manifest
:update_version
set "new_version=%~1"
call :print_status "Updating version to %new_version% in manifest.yml"

REM Create temporary file with updated version
powershell -Command "(Get-Content '%MANIFEST_FILE%') -replace '^version: .*', 'version: %new_version%' | Set-Content '%MANIFEST_FILE%'"

call :print_success "Version updated to %new_version%"
goto :eof

REM Function to build the project
:build_project
call :print_status "Building Alpaca4d.Gh project..."
cd /d "%PROJECT_ROOT%"

REM Build the project - use dotnet build on Windows for .NET Framework 4.8
dotnet build Alpaca4d.Gh\Alpaca4d.Gh.csproj --configuration Release

if errorlevel 1 (
    call :print_error "Project build failed"
    exit /b 1
)
call :print_success "Project built successfully"
goto :eof

REM Function to copy files to YAK directory
:copy_files_to_yak
call :print_status "Copying files to YAK directory..."

REM Create version directory
call :get_current_version
set "version_dir=%YAK_DIR%\%current_version%"
if not exist "%version_dir%" mkdir "%version_dir%"

REM Determine the correct output directory (SDK-style projects use net48 subdirectory)
set "output_dir=%PROJECT_ROOT%\Alpaca4d.Gh\bin\Release"
if exist "%output_dir%\net48" (
    set "output_dir=%output_dir%\net48"
    call :print_status "Using SDK-style output directory: %output_dir%"
)

REM Copy DLLs and GHA file
copy "%output_dir%\*.dll" "%version_dir%\" >nul 2>&1 || call :print_warning "No DLL files found in %output_dir%"
copy "%output_dir%\Alpaca4d.Gh.gha" "%version_dir%\" >nul 2>&1 || call :print_error "Alpaca4d.Gh.gha not found in %output_dir%"

REM Copy OpenSees-Solvers folder
if exist "%output_dir%\OpenSees-Solvers" (
    xcopy "%output_dir%\OpenSees-Solvers" "%version_dir%\OpenSees-Solvers\" /E /I /Y >nul
) else (
    call :print_warning "OpenSees-Solvers folder not found in %output_dir%"
)

REM Copy data.bin file
if exist "%output_dir%\data.bin" (
    copy "%output_dir%\data.bin" "%version_dir%\" >nul
) else (
    call :print_warning "data.bin file not found in %output_dir%"
)

REM Copy UserObject folder
if exist "%output_dir%\UserObject" (
    xcopy "%output_dir%\UserObject" "%version_dir%\UserObject\" /E /I /Y >nul
) else (
    call :print_warning "UserObject folder not found in %output_dir%"
)

call :print_success "Files copied to %version_dir%"
goto :eof

REM Function to build and push package
:build_and_push
call :print_status "Building package with yak..."

call :get_current_version
set "version_dir=%YAK_DIR%\%current_version%"

REM Copy manifest and icon to version directory for building
copy "%YAK_DIR%\manifest.yml" "%version_dir%\" >nul
copy "%YAK_DIR%\icon.png" "%version_dir%\" >nul

REM Build the package from within the version directory
cd /d "%version_dir%"

REM Temporarily rename .gha file to prevent Rhino version detection
REM This forces yak to use any-any instead of auto-detected rh7-any
if exist "Alpaca4d.Gh.gha" (
    ren "Alpaca4d.Gh.gha" "Alpaca4d.Gh.gha.temp"
    call :print_status "Temporarily renamed .gha file to force any-any distribution tag"
)

yak build --platform any

REM Restore the .gha file
if exist "Alpaca4d.Gh.gha.temp" (
    ren "Alpaca4d.Gh.gha.temp" "Alpaca4d.Gh.gha"
    call :print_status "Restored .gha file"
)

if errorlevel 1 (
    call :print_error "Failed to build package"
    exit /b 1
)
call :print_success "Package built successfully"

REM Find the built package in the version directory
for %%f in (*.yak) do (
    set "package_file=%%f"
    goto :found_package
)
call :print_error "No .yak package file found"
exit /b 1

:found_package
call :print_status "Package saved in: %version_dir%\!package_file!"
call :print_status "Pushing package: !package_file!"
yak push "!package_file!"

if errorlevel 1 (
    call :print_error "Failed to push package"
    exit /b 1
)
call :print_success "Package pushed successfully!"
goto :eof

REM Function to clean up
:cleanup
call :print_status "Cleaning up temporary files..."
call :get_current_version
set "version_dir=%YAK_DIR%\%current_version%"

if exist "%version_dir%" (
    REM Remove the copied manifest and icon, but keep the .yak file and binaries
    if exist "%version_dir%\manifest.yml" del "%version_dir%\manifest.yml"
    if exist "%version_dir%\icon.png" del "%version_dir%\icon.png"
    
    REM Remove all files except .yak files
    for /f "delims=" %%f in ('dir /b /a-d "%version_dir%\*" 2^>nul') do (
        if /i not "%%~xf"==".yak" del "%version_dir%\%%f"
    )
    
    REM Remove empty directories (but keep version directory with .yak file)
    for /f "delims=" %%d in ('dir /b /ad "%version_dir%" 2^>nul') do (
        rmdir "%version_dir%\%%d" 2>nul
    )
    
    call :print_success "Cleaned up temporary files, kept .yak package in %version_dir%"
)
goto :eof

REM Main execution
:main
call :print_status "Starting Alpaca4d plugin publishing process..."

REM Check prerequisites
call :check_yak
if errorlevel 1 exit /b 1

call :check_auth
if errorlevel 1 exit /b 1

REM Get current version
call :get_current_version
call :print_status "Current version: %current_version%"

REM Ask for new version
set /p "new_version=Enter new version (or press Enter to keep %current_version%): "

if "%new_version%"=="" set "new_version=%current_version%"

REM Update version if different
if not "%new_version%"=="%current_version%" (
    call :update_version "%new_version%"
)

REM Build project
call :build_project
if errorlevel 1 exit /b 1

REM Copy files
call :copy_files_to_yak

REM Build and push package
call :build_and_push
if errorlevel 1 exit /b 1

REM Cleanup
call :cleanup

call :print_success "Publishing process completed successfully!"
call :print_status "Package version %new_version% is now available on the Package Manager"
goto :eof

REM Run main function
call :main
pause
