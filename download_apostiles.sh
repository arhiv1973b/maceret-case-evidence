#!/bin/bash
# Download all apostiles from government site

mkdir -p apostiles

while IFS= read -r line; do
    # Extract code from URL
    code=$(echo "$line" | grep -oP '(?<=apostileCode/)[A-Z0-9]+')
    echo "Downloading: $code"
    curl -L -o "apostiles/${code}.pdf" "$line" 2>/dev/null
done < apostile_links.txt

echo "Download complete!"
