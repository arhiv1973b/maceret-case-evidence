import json
import hashlib
from pathlib import Path

root = Path(__file__).resolve().parent.parent
mp = root / "proofs" / "manifest.json"
print("Manifest path:", mp)

manifest = json.loads(mp.read_text(encoding="utf-8"))
manifest["manifest_version"] = "1.3.2"

for entry in manifest.get("files", []):
    p = root / entry["path"]
    if p.exists():
        entry["size_bytes"] = p.stat().st_size
        entry["sha256"] = hashlib.sha256(p.read_bytes()).hexdigest()
        print(
            f"Updated {entry['id']}: size={entry['size_bytes']}, sha256={entry['sha256']}"
        )
    else:
        print(f"Missing file: {p}")

mp.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
print("Successfully updated manifest!")
