#!/bin/bash
# Build and Push Docker Image to GHCR
# MACERET CASE EVIDENCE

set -e

echo "=== MACERET CASE EVIDENCE - Docker Build Script ==="

# Check if GHCR login is needed
if [ -z "$CR_PAT" ]; then
    echo "ERROR: Please set CR_PAT environment variable"
    echo "Run: export CR_PAT='your_github_token'"
    exit 1
fi

# Login to GHCR
echo "Logging in to GHCR..."
echo "$CR_PAT" | docker login ghcr.io -u arhiv1973b --password-stdin

# Build image
echo "Building Docker image..."
docker build -t ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21 .

# Push to GHCR
echo "Pushing to GHCR..."
docker push ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21
docker push ghcr.io/arhiv1973b/maceret-case-evidence:latest

# Get digest
echo "Image digest:"
docker inspect --format='{{index .RepoDigests 0}}' ghcr.io/arhiv1973b/maceret-case-evidence:v2026-02-21

echo "=== DONE ==="
