@echo off
rem launcher for VScode
call "%~dp0env_for_icons.bat"
cd/D "%WINPYWORKDIR%"
if exist "%WINPYDIR%\..\t\vscode\code.exe" (
    "%WINPYDIR%\..\t\vscode\code.exe" %*
) else (
if exist "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe" (
    "%LOCALAPPDATA%\Programs\Microsoft VS Code\code.exe"  %*
) else (
    "code.exe" %*
))

