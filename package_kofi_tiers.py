"""
Package Ko-fi Tier Releases
Generates:
1. Tier 1: PrivateDoc-RAG-Community-Edition-v2.2.zip (Personal use, Base setup)
2. Tier 2: PrivateDoc-RAG-Commercial-Pro-v2.2.zip (Commercial license, Docker, Sample docs)
"""

import os
import zipfile
from pathlib import Path

EXCLUDED_BASE = {
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".DS_Store",
    "Thumbs.db",
    "chroma_db",
    "dist",
}

def is_excluded(path: Path, root_dir: Path, exclude_samples: bool = False, exclude_docker: bool = False) -> bool:
    rel_parts = path.relative_to(root_dir).parts
    for part in rel_parts:
        if part in EXCLUDED_BASE or (part.startswith(".") and part not in (".gitignore", ".streamlit")):
            return True
        if part.endswith((".pyc", ".pyo", ".log")):
            return True
        if exclude_samples and part == "sample_docs":
            return True
        if exclude_docker and part in ("Dockerfile", "docker-compose.yml"):
            return True
    return False

def build_kofi_packages():
    root = Path(__file__).resolve().parent
    dist = root / "dist"
    dist.mkdir(exist_ok=True)

    # ── Tier 1: Community Edition ($0+ Pay-What-You-Want) ─────────────────────
    t1_zip = dist / "PrivateDoc-RAG-Community-Edition-v2.2.zip"
    print(f"[PACKAGING] Building Tier 1 Community Edition: {t1_zip.name}")
    t1_count = 0
    with zipfile.ZipFile(t1_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in root.rglob("*"):
            if f.is_file():
                if f.name in ("COMMERCIAL_LICENSE.md", "package_release.py", "package_kofi_tiers.py"):
                    continue
                if is_excluded(f, root, exclude_samples=True, exclude_docker=True):
                    continue
                arc = Path("PrivateDoc-RAG-Community") / f.relative_to(root)
                zipf.write(f, arc)
                t1_count += 1
    print(f"[DONE] Tier 1 created with {t1_count} files ({t1_zip.stat().st_size / 1024:.1f} KB)")

    # ── Tier 2: Commercial Pro Edition ($29 - $39) ────────────────────────────
    t2_zip = dist / "PrivateDoc-RAG-Commercial-Pro-v2.2.zip"
    print(f"[PACKAGING] Building Tier 2 Commercial Pro Edition: {t2_zip.name}")
    t2_count = 0
    with zipfile.ZipFile(t2_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for f in root.rglob("*"):
            if f.is_file():
                if f.name in ("package_release.py", "package_kofi_tiers.py"):
                    continue
                if is_excluded(f, root, exclude_samples=False, exclude_docker=False):
                    continue
                arc = Path("PrivateDoc-RAG-Commercial-Pro") / f.relative_to(root)
                zipf.write(f, arc)
                t2_count += 1
    print(f"[DONE] Tier 2 created with {t2_count} files ({t2_zip.stat().st_size / 1024:.1f} KB)")

if __name__ == "__main__":
    build_kofi_packages()
