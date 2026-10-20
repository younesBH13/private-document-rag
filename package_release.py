"""
Package Release Script
Bundles the PrivateDoc RAG project into a clean, distributable .zip archive
suitable for upload to Gumroad or client delivery.
"""

import os
import zipfile
from pathlib import Path

# Files and directories to strictly exclude
EXCLUDED_PATTERNS = {
    ".git",
    ".github",
    ".pytest_cache",
    "__pycache__",
    ".venv",
    "venv",
    "env",
    ".DS_Store",
    "Thumbs.db",
    "*.pyc",
    "*.pyo",
    "*.log",
    "chroma_db",
    "dist",
}

def is_excluded(path: Path, root_dir: Path) -> bool:
    rel_parts = path.relative_to(root_dir).parts
    for part in rel_parts:
        if part in EXCLUDED_PATTERNS or part.startswith(".") and part != ".gitignore":
            return True
        if part.endswith((".pyc", ".pyo", ".log")):
            return True
    return False

def build_zip():
    project_root = Path(__file__).resolve().parent
    dist_dir = project_root / "dist"
    dist_dir.mkdir(exist_ok=True)
    
    zip_filename = dist_dir / "PrivateDoc-RAG-v1.0-Turnkey-Boilerplate.zip"
    
    print(f"[PACKAGING] PrivateDoc RAG from: {project_root}")
    print(f"[OUTPUT] Archive: {zip_filename}")
    
    count = 0
    with zipfile.ZipFile(zip_filename, "w", zipfile.ZIP_DEFLATED) as zipf:
        for file_path in project_root.rglob("*"):
            if file_path.is_file():
                if is_excluded(file_path, project_root):
                    continue
                # Add to zip with relative path inside a top-level folder
                arcname = Path("private-document-rag") / file_path.relative_to(project_root)
                zipf.write(file_path, arcname)
                count += 1
                
    file_size_kb = zip_filename.stat().st_size / 1024
    print(f"[SUCCESS] Packaged {count} files successfully!")
    print(f"[INFO] Zip file size: {file_size_kb:.1f} KB")
    print(f"[READY] Upload to Gumroad: {zip_filename}")

if __name__ == "__main__":
    build_zip()
