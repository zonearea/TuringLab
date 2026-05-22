# TuringLab video kaydı — UTF-8 terminal + demo
$ErrorActionPreference = "Stop"
Set-Location $PSScriptRoot\..

chcp 65001 | Out-Null
Write-Host "TuringLab video demo (UTF-8)" -ForegroundColor Cyan
Write-Host "Kullanim: python scripts/demo_video.py --section N  veya  --all`n"

if ($args.Count -gt 0) {
    python scripts/demo_video.py @args
} else {
    python scripts/demo_video.py --all
}
