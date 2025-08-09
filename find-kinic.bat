@echo off
echo Opening Kinic Position Finder...
powershell.exe -ExecutionPolicy Bypass -File "%~dp0get-exact-position.ps1"
pause