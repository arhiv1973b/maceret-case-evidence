# Auto-Sync Configuration for maceret-case-evidence
# Source folder: C:\Users\arhiv\upload_archive
# Target: https://github.com/arhiv1973b/maceret-case-evidence

SYNC_SOURCE="C:/Users/arhiv/upload_archive"
GITHUB_REPO="https://github.com/arhiv1973b/maceret-case-evidence.git"
CHECK_INTERVAL=300  # seconds

# Files to always sync
SYNC_FILES=(
    "*.md"
    "*.pdf"
    "*.txt"
    "*.json"
    "*.sh"
)

# Log file
LOG_FILE="C:/Users/arhiv/sync_log.txt"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

sync_now() {
    cd "$SYNC_SOURCE"
    
    # Check for changes
    if git diff --quiet && git diff --staged --quiet; then
        log "No changes detected"
        return
    fi
    
    log "Changes detected, committing..."
    
    # Add all files
    git add -A
    
    # Commit with timestamp
    git commit -m "Auto-sync: $(date '+%Y-%m-%d %H:%M:%S')"
    
    # Push
    if git push origin main 2>&1 | tee -a "$LOG_FILE"; then
        log "Push successful"
    else
        log "Push failed - retrying..."
        git pull origin main --allow-unrelated-histories
        git push origin main
    fi
}

# Initial sync
log "Auto-sync service started"
sync_now

# Watch mode (using while loop as简易cron)
while true; do
    sleep $CHECK_INTERVAL
    sync_now
done
