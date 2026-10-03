#Requires -Version 7.0
# 从 iCloud 文献库/ 按文件名恢复 literature/**/sources/ 下的论文 PDF。
# 目标位置取自译文页 frontmatter 的 source: 字段，以及 literature/refs.bib 中 note 的「本地 PDF <仓库相对路径>」。
# 只复制缺失文件，不覆盖、不删除。
[CmdletBinding()]
param(
    [switch]$Preview
)

Set-StrictMode -Version Latest
$ErrorActionPreference = 'Stop'

$repo = $PSScriptRoot
$literature = Join-Path $repo 'literature'
$pool = Join-Path $env:USERPROFILE 'iCloudDrive\文献库'

try {
    if (-not (Test-Path -LiteralPath $pool -PathType Container)) {
        throw "iCloud 文献库 not found: $pool"
    }

    $targets = [ordered]@{}

    Get-ChildItem -LiteralPath $literature -Recurse -File -Filter '*-zh.md' | ForEach-Object {
        $m = Select-String -LiteralPath $_.FullName -Pattern '^source:\s*["'']?([^"''#\s]+\.pdf)' -List
        if ($m) {
            $full = [IO.Path]::GetFullPath((Join-Path $_.DirectoryName $m.Matches[0].Groups[1].Value))
            $targets[$full] = $true
        }
    }

    $bib = Join-Path $literature 'refs.bib'
    Select-String -LiteralPath $bib -Pattern '本地 PDF\s+(literature/[^\s,;}]+\.pdf)' -AllMatches | ForEach-Object {
        foreach ($match in $_.Matches) {
            $full = [IO.Path]::GetFullPath((Join-Path $repo $match.Groups[1].Value))
            $targets[$full] = $true
        }
    }

    $present = 0
    $restored = 0
    $missing = @()

    foreach ($target in $targets.Keys) {
        $name = Split-Path -Leaf $target
        $src = Join-Path $pool $name
        if (Test-Path -LiteralPath $target -PathType Leaf) {
            $present++
        }
        elseif (-not (Test-Path -LiteralPath $src -PathType Leaf)) {
            $missing += $name
        }
        else {
            if (-not $Preview) {
                $null = New-Item -ItemType Directory -Path (Split-Path -Parent $target) -Force
                Copy-Item -LiteralPath $src -Destination $target
            }
            Write-Host "RESTORE $([IO.Path]::GetRelativePath($repo, $target))"
            $restored++
        }
    }

    $unregistered = Get-ChildItem -LiteralPath $literature -Recurse -File -Filter '*.pdf' |
        Where-Object { $_.Directory.Name -eq 'sources' -and -not $targets.Contains($_.FullName) }

    foreach ($f in $unregistered) {
        Write-Host "UNREGISTERED $([IO.Path]::GetRelativePath($repo, $f.FullName))" -ForegroundColor Yellow
    }
    foreach ($name in $missing) {
        Write-Host "MISSING IN POOL $name" -ForegroundColor Red
    }

    $mode = if ($Preview) { 'Preview' } else { 'Copy' }
    Write-Host "[$mode] registered: $($targets.Count)  present: $present  restored: $restored  missing: $($missing.Count)  unregistered: $(@($unregistered).Count)"

    if ($missing.Count -gt 0) { exit 1 }
    exit 0
}
catch {
    Write-Error ("Restore failed: {0}" -f $_.Exception.Message)
    exit 1
}
