@echo off
call "%~dp0env_for_icons.bat"
cd/D "%WINPYWORKDIR%"
if "%QT_API%"=="pyqt5" (
    if exist "%WINPYDIR%\Lib\site-packages\pyqt5-tools\assistant.exe" (
        "%WINPYDIR%\Lib\site-packages\pyqt5-tools\assistant.exe" %*
    ) else if exist "%WINPYDIR%\Lib\site-packages\PyQt5\assistant.exe" (
        "%WINPYDIR%\Lib\site-packages\PyQt5\assistant.exe" %*
    ) else (
        "%WINPYDIR%\Lib\site-packages\PySide2\designer.exe" %*
    )
) else (
    "%WINPYDIR%\Lib\site-packages\PySide2\designer.exe" %*
)
