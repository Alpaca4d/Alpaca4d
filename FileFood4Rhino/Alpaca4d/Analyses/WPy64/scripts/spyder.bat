@echo off
call "%~dp0env_for_icons.bat"
cd/D "%WINPYWORKDIR%"
if exist "%WINPYDIR%\scripts\spyder3.exe" (
   "%WINPYDIR%\scripts\spyder3.exe" %*
) else (
   "%WINPYDIR%\scripts\spyder.exe" %*
)   
