[CmdletBinding()]
param(
    [switch]$Preview
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$source = $PSScriptRoot
$repoName = Split-Path -Leaf $source
$userProfile = $env:USERPROFILE
$iCloudDrive = Join-Path $userProfile 'iCloudDrive'
$destParent = Join-Path $iCloudDrive 'iCloud~md~obsidian'
$dest = Join-Path $destParent $repoName

try {
    if (-not (Test-Path -LiteralPath $iCloudDrive -PathType Container)) {
        throw "iCloud Drive folder not found: $iCloudDrive"
    }

    $robocopy = Get-Command robocopy.exe -ErrorAction Stop

    if (-not $Preview -and -not (Test-Path -LiteralPath $destParent -PathType Container)) {
        $null = New-Item -ItemType Directory -Path $destParent -Force
    }

    Write-Host "=== Syncing $repoName to iCloud Obsidian ===" -ForegroundColor Cyan
    Write-Host "Source:      $source"
    Write-Host "Destination: $dest"
    Write-Host "Mode:        $(if ($Preview) { 'Preview (/L)' } else { 'Mirror (/MIR)' })"

    $robocopyParams = @(
        $source,
        $dest,
        '/MIR',
        '/XD', '.git', '.agents', '.claude', '.codex',
        '/XF', '.gitignore', 'AGENTS.md', 'CLAUDE.md', 'GEMINI.md', 'texput.log', '*.tmp', '*.ps1',
        '/R:1',
        '/W:1',
        '/NP'
    )

    if ($Preview) {
        $robocopyParams += '/L'
    }

    & $robocopy.Source @robocopyParams
    $robocopyExitCode = $LASTEXITCODE

    if ($robocopyExitCode -le 7) {
        Write-Host "[SUCCESS] Robocopy code: $robocopyExitCode" -ForegroundColor Green
        exit 0
    }

    Write-Host "[ERROR] Robocopy code: $robocopyExitCode" -ForegroundColor Red
    exit $robocopyExitCode
}
catch {
    Write-Error ("Sync failed: {0}" -f $_.Exception.Message)
    exit 1
}
