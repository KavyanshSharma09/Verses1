param(
    [string]$BackupFile = "",
    [switch]$SkipExport,
    [string]$TargetDatabaseUrl = ""
)

$ErrorActionPreference = "Stop"

function Invoke-CheckedCommand {
    param(
        [string]$Program,
        [string[]]$Arguments,
        [string]$StepName
    )

    & $Program @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "$StepName failed with exit code $LASTEXITCODE."
    }
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
    throw "DATABASE_URL is not set. Export your PostgreSQL connection string (Supabase/Render), then rerun this script."
}

if (-not $SkipExport) {
    # Force source export from local SQLite by removing DATABASE_URL temporarily.
    Remove-Item Env:DATABASE_URL -ErrorAction SilentlyContinue
    $env:DEBUG = "True"

    if (-not (Test-Path "backups")) {
        New-Item -ItemType Directory -Path "backups" | Out-Null
    }

    if (-not $BackupFile) {
        $ts = Get-Date -Format yyyyMMdd-HHmmss
        $BackupFile = "backups/backup-$ts.json"
    }

    Invoke-CheckedCommand -Program $python -Arguments @(
        'manage.py',
        'dumpdata',
        '--natural-foreign',
        '--natural-primary',
        '--exclude', 'contenttypes',
        '--exclude', 'auth.permission',
        '--output', $BackupFile
    ) -StepName 'SQLite export'
}

if (-not $BackupFile) {
    $latest = Get-ChildItem "backups/backup-*.json" -ErrorAction SilentlyContinue | Sort-Object LastWriteTime -Descending | Select-Object -First 1
    if (-not $latest) {
        throw "No backup file found in backups/. Provide -BackupFile or run without -SkipExport."
    }
    $BackupFile = $latest.FullName
}

if (-not (Test-Path $BackupFile)) {
    throw "Backup file not found: $BackupFile"
}

Write-Output "Using backup file: $BackupFile"
Write-Output "Switching connection to target PostgreSQL..."
$env:DATABASE_URL = $targetDbUrl
$env:DEBUG = "False"
Write-Output "Running migrations on PostgreSQL..."
Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'migrate') -StepName 'PostgreSQL migrate'

Write-Output "Loading backup into PostgreSQL..."
Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'loaddata', $BackupFile) -StepName 'PostgreSQL loaddata'

Write-Output "Running post-load checks..."
Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'check') -StepName 'Django check'
Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'showmigrations') -StepName 'Show migrations'

$countsScript = @'
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
print(json.dumps(counts, indent=2, sort_keys=True))
'@

Write-Output "PostgreSQL row counts:"
Invoke-CheckedCommand -Program $python -Arguments @('manage.py', 'shell', '-c', $countsScript) -StepName 'PostgreSQL counts'

Write-Output "SQLite -> PostgreSQL migration completed."
