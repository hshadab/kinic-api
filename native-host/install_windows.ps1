Param(
  [string]$HostName = 'com.kinic.api'
)

$ErrorActionPreference = 'Stop'

# Install Kinic native host manifest for Windows (user scope)
# Registry key: HKCU:\Software\Google\Chrome\NativeMessagingHosts\<HostName>

$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
$HostBat   = Join-Path $ScriptDir 'kinic_native_host.bat'
$ManifestTemplate = Join-Path $ScriptDir 'manifest\windows\com.kinic.api.json'

if (-not (Test-Path $HostBat)) {
  Write-Error "Host launcher not found: $HostBat"
}

if (-not (Test-Path $ManifestTemplate)) {
  Write-Error "Manifest template not found: $ManifestTemplate"
}

# Choose a manifest path in user profile
$ManifestDir  = Join-Path $env:LOCALAPPDATA 'Kinic\\NativeMessagingHosts'
$ManifestPath = Join-Path $ManifestDir "$HostName.json"
New-Item -ItemType Directory -Force -Path $ManifestDir | Out-Null

# Replace absolute path placeholder
$content = Get-Content $ManifestTemplate -Raw
$content = $content.Replace('C:\\ABSOLUTE\\PATH\\TO\\kinic_native_host.bat', $HostBat)
Set-Content -Path $ManifestPath -Value $content -Encoding ASCII

# Registry key
$RegPath = "HKCU:\\Software\\Google\\Chrome\\NativeMessagingHosts\\$HostName"
New-Item -Path $RegPath -Force | Out-Null
New-ItemProperty -Path $RegPath -Name '(Default)' -Value $ManifestPath -PropertyType String -Force | Out-Null

Write-Output "Installed manifest: $ManifestPath"
Write-Output "Registry: $RegPath"
Write-Output "Replace DEV_EXTENSION_ID and PROD_EXTENSION_ID in the manifest as needed."

