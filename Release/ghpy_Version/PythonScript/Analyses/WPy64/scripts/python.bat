@echo off
call "%~dp0env_for_icons.bat"
rem backward compatibility for  python command-line users
"%WINPYDIR%\python.exe"  %*
