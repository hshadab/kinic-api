# PowerShell script to get exact mouse position
Add-Type -AssemblyName System.Windows.Forms
Add-Type -AssemblyName System.Drawing

Write-Host "KINIC POSITION FINDER" -ForegroundColor Cyan
Write-Host "=====================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Instructions:" -ForegroundColor Yellow
Write-Host "1. Move your mouse over the Kinic button"
Write-Host "2. Press SPACE to capture position"
Write-Host "3. Press Q to quit"
Write-Host ""
Write-Host "Tracking mouse position..." -ForegroundColor Green
Write-Host ""

$captured = $false
$lastPos = $null

while (-not $captured) {
    $pos = [System.Windows.Forms.Cursor]::Position
    
    # Only update display if position changed
    if ($lastPos -eq $null -or $pos.X -ne $lastPos.X -or $pos.Y -ne $lastPos.Y) {
        Write-Host "`rX: $($pos.X), Y: $($pos.Y)    " -NoNewline
        $lastPos = $pos
    }
    
    # Check for key press
    if ([System.Console]::KeyAvailable) {
        $key = [System.Console]::ReadKey($true)
        
        if ($key.Key -eq "Spacebar") {
            Write-Host ""
            Write-Host ""
            Write-Host "CAPTURED!" -ForegroundColor Green
            Write-Host "Kinic button position: X=$($pos.X), Y=$($pos.Y)" -ForegroundColor Cyan
            Write-Host ""
            Write-Host "To update your config, run:" -ForegroundColor Yellow
            Write-Host "curl -X POST http://localhost:5003/setup -H `"Content-Type: application/json`" -d '{`"x`":$($pos.X),`"y`":$($pos.Y)}'" -ForegroundColor White
            $captured = $true
        }
        elseif ($key.Key -eq "Q") {
            Write-Host ""
            Write-Host "Cancelled" -ForegroundColor Red
            break
        }
    }
    
    Start-Sleep -Milliseconds 50
}

Write-Host ""
Write-Host "Press any key to exit..."
[System.Console]::ReadKey($true) | Out-Null