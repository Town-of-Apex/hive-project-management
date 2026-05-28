param(
    [switch]$SkipSeed
)

$ErrorActionPreference = "Stop"
$Root = $PSScriptRoot
Set-Location $Root

Write-Host ""
Write-Host 'Hive Project Management — Dev Mode'
Write-Host ""

# Virtual environment
if (-not (Test-Path '.\.venv\Scripts\python.exe')) {
    Write-Host 'Creating virtual environment...'
    python -m venv .venv
}

$Python = '.\.venv\Scripts\python.exe'
$Pip = '.\.venv\Scripts\pip.exe'

Write-Host 'Installing Python dependencies...'
& $Pip install -q -r requirements.txt

# PostgreSQL container
Write-Host 'Starting PostgreSQL (apex-db)...'
$networkExists = docker network inspect apex-internal 2>$null
if (-not $networkExists) {
    Write-Host "Creating docker network apex-internal..."
    docker network create apex-internal | Out-Null
}
docker compose up -d apex-db | Out-Null

Write-Host 'Waiting for PostgreSQL on localhost:5432...'
$ready = $false
for ($i = 0; $i -lt 30; $i++) {
    try {
        $tcp = New-Object System.Net.Sockets.TcpClient
        $tcp.Connect("localhost", 5432)
        $tcp.Close()
        $ready = $true
        break
    } catch {
        Start-Sleep -Seconds 1
    }
}
if (-not $ready) {
    throw 'PostgreSQL did not become ready on port 5432. Is apex-db running?'
}

# Host dev always targets local apex-db (override .env DATABASE_URL if misconfigured)
$env:DATABASE_URL = 'postgresql+psycopg://postgres:postgres@localhost:5432/apex_db'
$env:ALLOW_SQLITE_FALLBACK = 'false'

# Load optional .env for JWT_SECRET and other settings (not DATABASE_URL)
if (Test-Path '.\.env') {
    Get-Content '.\.env' | ForEach-Object {
        if ($_ -match '^\s*([^#][^=]+)=(.*)$') {
            $key = $matches[1].Trim()
            if ($key -ne "DATABASE_URL" -and $key -ne "ALLOW_SQLITE_FALLBACK") {
                [System.Environment]::SetEnvironmentVariable($key, $matches[2].Trim(), "Process")
            }
        }
    }
}

Write-Host 'Running database migrations...'
& $Python -m alembic upgrade head

if (-not $SkipSeed) {
    Write-Host 'Seeding development data...'
    & $Python scripts/seed_dev.py
} else {
    Write-Host 'Skipping seed (-SkipSeed).'
}

# Backend in new window
$backendCmd = @"
Set-Location '$Root'
`$env:DATABASE_URL = 'postgresql+psycopg://postgres:postgres@localhost:5432/apex_db'
`$env:ALLOW_SQLITE_FALLBACK = 'false'
.\.venv\Scripts\Activate.ps1
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
"@

Start-Process powershell.exe -ArgumentList '-NoExit', '-Command', $backendCmd

# Frontend in current window
Write-Host ""
Write-Host 'Starting frontend (Vite :5173)...'
Write-Host 'Open http://localhost:5173 and sign in with devadmin / devadmin123'
Write-Host ""
Set-Location frontend

npm run dev
