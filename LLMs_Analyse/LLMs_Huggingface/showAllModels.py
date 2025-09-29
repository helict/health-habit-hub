import os
from pathlib import Path

cache_dir = Path.home() / ".cache" / "huggingface" / "hub"
repos = [d for d in cache_dir.glob("models--*") if d.is_dir()]
for repo in repos:
    print(repo.name)
