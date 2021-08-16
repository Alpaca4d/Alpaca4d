@echo off
call "%~dp0env_for_icons.bat"
cd/D "%WINPYWORKDIR%"
if "%QT_API%"=="pyqt5" (
    if exist "%WINPYDIR%\Lib\site-packages\pyqt5-tools\linguist.exe" (
        "%WINPYDIR%\Lib\site-packages\pyqt5-tools\linguist.exe" %*
    ) else if exist "%WINPYDIR%\Lib\site-packages\pyqt5_tools\linguist.exe" (
        "%WINPYDIR%\Lib\site-packages\pyqt5_tools\linguist.exe" %*
    ) else (
        cd/D "%WINPYDIR%\Lib\site-packages\PyQt5"
        "%WINPYDIR%\Lib\site-packages\PyQt5\linguist.exe" %*
    )
) else (
    "%WINPYDIR%\Lib\site-packages\PySide2\linguist.exe" %*
)

