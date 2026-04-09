"""
Quick cache diagnostic - finds all HuggingFace models already downloaded.
Run this first to confirm which models are available before running the main notebooks.
"""
import os
import json
from pathlib import Path

CANDIDATE_CACHE_DIRS = [
    Path(os.environ.get("HF_HOME", "")) / "hub",
    Path(os.environ.get("HUGGINGFACE_HUB_CACHE", "")),
    Path.home() / ".cache" / "huggingface" / "hub",
    Path("D:/") / ".cache" / "huggingface" / "hub",
    Path("D:/") / "huggingface" / "hub",
    Path("D:/hf_cache"),
]

found_models = []

for cache_dir in CANDIDATE_CACHE_DIRS:
    if cache_dir.exists():
        print(f"\n✅ Cache found at: {cache_dir}")
        for entry in sorted(cache_dir.iterdir()):
            if entry.is_dir() and entry.name.startswith("models--"):
                model_id = entry.name.replace("models--", "").replace("--", "/")
                # Check size
                size_gb = sum(f.stat().st_size for f in entry.rglob("*") if f.is_file()) / 1e9
                found_models.append({"model": model_id, "path": str(entry), "size_gb": round(size_gb, 2)})
                print(f"  📦 {model_id}  ({size_gb:.2f} GB)")
    else:
        print(f"❌ Not found: {cache_dir}")

print(f"\n\n{'='*60}")
print(f"SUMMARY: {len(found_models)} cached models found")
print(f"{'='*60}")

# Save as JSON for the notebook to read
with open("cached_models.json", "w") as f:
    json.dump(found_models, f, indent=2)
print("Saved to cached_models.json")
