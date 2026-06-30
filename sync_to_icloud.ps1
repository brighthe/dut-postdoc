# sync_to_icloud.ps1
# This script performs a one-way sync from this repository to iCloud Drive's Obsidian container.
# Place this script in the root of your repository (e.g., C:\workspace\dut-postdoc\sync_to_icloud.ps1).
# It will dynamically detect its own location as the source.

# 1. Dynamically determine the source folder path (where this script is located)
$source = $PSScriptRoot
$repoName = Split-Path -Leaf $source

$iCloudDrive = Join-Path $env:USERPROFILE "iCloudDrive"
$destParent = Join-Path $iCloudDrive "iCloud~md~obsidian"
$dest = Join-Path $destParent $repoName

Write-Host "=== Syncing $repoName to iCloud Obsidian Container ===" -ForegroundColor Cyan
Write-Host "Source (Local & Git): $source"
Write-Host "Destination (iCloud):  $dest"
Write-Host "========================================================"

# 2. Check if iCloudDrive exists
if (-not (Test-Path $iCloudDrive)) {
    Write-Host "[ERROR] iCloud Drive folder not found at $iCloudDrive" -ForegroundColor Red
    Write-Host "Please make sure iCloud for Windows is installed and logged in." -ForegroundColor Yellow
    exit 1
}

# 3. Create parent container folder if it doesn't exist
if (-not (Test-Path $destParent)) {
    Write-Host "Creating parent folder: $destParent" -ForegroundColor Gray
    New-Item -ItemType Directory -Path $destParent -Force | Out-Null
}

Write-Host "Starting sync using Windows Robocopy..." -ForegroundColor Yellow
Write-Host "Config: Mirror mode. Excluding Git metadata (.git) and script itself." -ForegroundColor Gray
Write-Host ""

# Robocopy Options:
# /MIR: Mirror directory tree (copies new/modified, deletes files in dest if deleted in source)
# /XD: Exclude directories (.git and .agents)
# /XF: Exclude developer files (.gitignore, CLAUDE.md, etc.) and this script itself (*.ps1)
$params = @(
    $source,
    $dest,
    "/MIR",
    "/XD", ".git", ".agents",
    "/XF", ".gitignore", "AGENTS.md", "CLAUDE.md", "texput.log", "*.tmp", "*.ps1",
    "/R:1",
    "/W:1"
)

# Run Robocopy
& robocopy @params

# Robocopy Exit Codes:
# Codes 0-7 mean success
$exitCode = $LASTEXITCODE

if ($exitCode -lt 8) {
    Write-Host ""
    Write-Host "[SUCCESS] Sync completed successfully! (Robocopy Code: $exitCode)" -ForegroundColor Green
    Write-Host "- Local folder and Git history remain untouched." -ForegroundColor Gray
    Write-Host "- iCloud now has the latest documents, fully updated and ready for mobile viewing." -ForegroundColor Gray
} else {
    Write-Host ""
    Write-Host "[WARNING] Sync completed with warnings/errors (Robocopy Code: $exitCode)." -ForegroundColor Yellow
    Write-Host "Some files may be locked by other applications (e.g. Obsidian or PDF reader)." -ForegroundColor Yellow
}
