param(
    [string]$TargetDatabaseUrl = ""
)

$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand {
    param(
        [string]$Program,
        [string[]]$Arguments,
        [string]$StepName
    )

    $output = & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$StepName failed with exit code $LASTEXITCODE."
    }

    return $output
}

$projectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $projectRoot

$python = "E:/Projects/Verses 1/.venv/Scripts/python.exe"
if (-not (Test-Path $python)) {
    $python = "python"
}

$env:PYTHONUTF8 = "1"

$targetDbUrl = if ($TargetDatabaseUrl) { $TargetDatabaseUrl } else { $env:DATABASE_URL }
if (-not $targetDbUrl) {
    throw "DATABASE_URL is not set. Provide -TargetDatabaseUrl or set DATABASE_URL in environment."
}

if (-not (Test-Path "backups")) {
    New-Item -ItemType Directory -Path "backups" | Out-Null
}

$countScript = @'
import json
from django.contrib.auth.models import User
from battles.models import Battle, CodeSubmission, BattleResult, Category, ProblemStatement, TestCase, PracticeSubmission, UserStats, LoginActivity
from upload.models import UploadFile

counts = {
    'users': User.objects.count(),
    'categories': Category.objects.count(),
    'problems': ProblemStatement.objects.count(),
    'test_cases': TestCase.objects.count(),
    'battles': Battle.objects.count(),
    'code_submissions': CodeSubmission.objects.count(),
    'battle_results': BattleResult.objects.count(),
    'practice_submissions': PracticeSubmission.objects.count(),
    'user_stats': UserStats.objects.count(),
    'login_activity': LoginActivity.objects.count(),
    'uploaded_files': UploadFile.objects.count(),
}
print(json.dumps(counts, sort_keys=True))
'@

Write-Output "Collecting source counts from local SQLite..."
Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
$env:DEBUG = "True"
$sourceRaw = Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'shell', '-v', '0', '-c', $countScript) -StepName 'SQLite count collection'
$sourceJson = ($sourceRaw -join "`n")
$sourceCounts = $sourceJson | ConvertFrom-Json

Write-Output "Collecting target counts from PostgreSQL..."
$env:DATABASE_URL = $targetDbUrl
$env:DEBUG = "False"
$targetRaw = Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'shell', '-v', '0', '-c', $countScript) -StepName 'PostgreSQL count collection'
$targetJson = ($targetRaw -join "`n")
$targetCounts = $targetJson | ConvertFrom-Json

$keys = @($sourceCounts.PSObject.Properties.Name + $targetCounts.PSObject.Properties.Name | Sort-Object -Unique)
$differences = @()
foreach ($k in $keys) {
    $s = [int]($sourceCounts.$k)
    $t = [int]($targetCounts.$k)
    if ($s -ne $t) {
        $differences += [pscustomobject]@{
            table = $k
            source = $s
            target = $t
            delta = $t - $s
        }
    }
}

$ts = Get-Date -Format yyyyMMdd-HHmmss
$reportPath = "backups/migration-verify-$ts.json"
$report = [pscustomobject]@{
    timestamp = (Get-Date).ToString('o')
    source = 'sqlite'
    target = 'postgresql'
    source_counts = $sourceCounts
    target_counts = $targetCounts
    matches = ($differences.Count -eq 0)
    differences = $differences
}
$report | ConvertTo-Json -Depth 8 | Set-Content -Path $reportPath -Encoding UTF8

Write-Output "Verification report: $reportPath"
if ($differences.Count -eq 0) {
    Write-Output "All table counts match between SQLite and PostgreSQL."
} else {
    Write-Output "Count differences found:"
    $differences | Format-Table -AutoSize
    throw "SQLite and PostgreSQL counts do not match."
}
