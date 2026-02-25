# Auto-Sync Service - README

## Status: ACTIVE ✓
**Repository:** https://github.com/arhiv1973b/maceret-case-evidence

## How It Works

### Option 1: Windows Background Service
```batch
# Run this to start auto-sync (as administrator)
auto_sync.bat
```

### Option 2: Windows Task Scheduler
```cmd
schtasks /create /tn "MaceretCaseSync" /tr "C:\Users\arhiv\upload_archive\auto_sync.bat" /sc minute /mo 5
```

### Option 3: Manual Sync
```bash
cd C:\Users\arhiv\upload_archive
git add -A
git commit -m "Manual sync: $(date)"
git push origin main
```

## Current Status
- Auto-sync: ENABLED
- Check interval: 5 minutes
- Log file: C:\Users\arhiv\sync_log.txt

## Files Tracked
All files in `upload_archive/` folder are automatically synced.

## To Add New Files
Simply copy files to `C:\Users\arhiv\upload_archive\` - they will be synced automatically.

## Manual Override
Push directly from any Git client:
```bash
git -C "C:\Users\arhiv\upload_archive" push origin main
```
