# GHCR Setup Instructions

## Prerequisites

1. GitHub Account: arhiv1973b
2. PAT Token with: repo, write:packages, read:packages

## Quick Start

### Option 1: PowerShell

```powershell
$env:CR_PAT = "your_github_pat_token"
.\build-ghcr.ps1
```

### Option 2: Bash/WSL

```bash
export CR_PAT="your_github_pat_token"
chmod +x build-ghcr.sh
./build-ghcr.sh
```

## Manual Build

```bash
# Login
echo $CR_PAT | docker login ghcr.io -u arhiv1973b --password-stdin

# Build
docker build -t ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21 .

# Push
docker push ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21
docker push ghcr.io/arhiv1973b/maceret-case-evidence:latest

# Verify
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/arhiv1973b/maceret-case-evidence:latest
```

## Get PAT Token

1. Go to: https://github.com/settings/tokens
2. Generate new token (Classic)
3. Select scopes: repo, write:packages, read:packages, delete:packages
4. Copy token and use in commands above

---

Updated: 2026-02-21
