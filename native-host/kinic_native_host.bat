@echo off
setlocal
REM Kinic Native Host launcher for Windows (calls Python 3 with unbuffered stdio)
set SCRIPT_DIR=%~dp0
py -3 -u "%SCRIPT_DIR%kinic_native_host.py" %*
endlocal

