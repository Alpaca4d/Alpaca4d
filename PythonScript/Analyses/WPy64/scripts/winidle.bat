@echo off
call "%~dp0env_for_icons.bat"
cd/D "%WINPYWORKDIR%"
"%WINPYDIR%\python.exe" "%WINPYDIR%\Lib\idlelib\idle.pyw" %*
