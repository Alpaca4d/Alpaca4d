@echo off
set winpython_ini=%~dp0..\\settings\winpython.ini
(
    echo [debug]
    echo state = disabled
    echo [environment]
    echo ## <?> Uncomment lines to override environment variables
    echo HOME = %%HOMEDRIVE%%%%HOMEPATH%%\Documents\WinPython%%WINPYVER%%\settings
    echo USERPROFILE = %%HOME%%
    echo JUPYTER_DATA_DIR = %%HOME%%
    echo WINPYWORKDIR = %%HOMEDRIVE%%%%HOMEPATH%%\Documents\WinPython%%WINPYVER%%\Notebooks
) > "%winpython_ini%"
    call "%~dp0env_for_icons.bat"
    mkdir %HOMEDRIVE%%HOMEPATH%\Documents\WinPython%WINPYVER%\settings
    mkdir %HOMEDRIVE%%HOMEPATH%\Documents\WinPython%WINPYVER%\settings\AppData
    mkdir %HOMEDRIVE%%HOMEPATH%\Documents\WinPython%WINPYVER%\settings\AppData\Roaming
