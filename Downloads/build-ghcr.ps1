# Build and Push Docker Image to GHCR
# MACERET CASE EVIDENCE

$ErrorActionPreference = "Stop"

Write-Host "=== MACERET CASE EVIDENCE - Docker Build Script ===" -ForegroundColor Cyan

# Check if GHCR login is needed
if (-not $env:CR_PAT) {
    Write-Host "ERROR: Please set CR_PAT environment variable" -ForegroundColor Red
    Write-Host "Run: `$env:CR_PAT = 'your_github_token'" -ForegroundColor Yellow
    exit 1
}

# Login to GHCR
Write-Host "Logging in to GHCR..." -ForegroundColor Yellow
$env:CR_PAT | docker login ghcr.io -u arhiv1973b --password-stdin

# Get script directory
$ScriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Build image
Write-Host "Building Docker image..." -ForegroundColor Yellow
docker build -t ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21 $ScriptDir

# Push to GHCR
Write-Host "Pushing to GHCR..." -ForegroundColor Yellow
docker push ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21
docker push ghcr.io/arhiv1973b/maceret-case-evidence:latest

# Get digest
Write-Host "Image digest:" -ForegroundColor Cyan
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21

Write-Host "=== DONE ===" -ForegroundColor Green
