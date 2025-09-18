$ErrorActionPreference = 'Stop'

$HostName = 'com.kinic.api'
$RegPath  = "HKCU:\\Software\\Google\\Chrome\\NativeMessagingHosts\\$HostName"

try {
  if (Test-Path $RegPath) {
    Remove-Item -Path $RegPath -Recurse -Force
    Write-Output "Removed registry key: $RegPath"
  } else {
    Write-Output "Registry key not found: $RegPath"
  }
} catch {
  Write-Warning "Failed to remove registry key: $_"
}

$ManifestPath = Join-Path $env:LOCALAPPDATA 'Kinic\\NativeMessagingHosts\\com.kinic.api.json'
if (Test-Path $ManifestPath) {
  Remove-Item -Path $ManifestPath -Force
  Write-Output "Removed manifest: $ManifestPath"
} else {
  Write-Output "Manifest not found: $ManifestPath"
}

Write-Output "If you installed manifests in other locations (Edge/Chrome Beta), remove those too."

