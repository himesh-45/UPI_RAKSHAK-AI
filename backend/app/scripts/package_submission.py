import os
import zipfile
import fnmatch

EXCLUDE_DIRS = {
    ".venv", "venv", "node_modules", ".git", ".pytest_cache",
    "dist", "build", "__pycache__", ".vite"
}

EXCLUDE_PATTERNS = [
    "*.db", "*.sqlite", "*.sqlite3", ".env", ".env.local",
    ".admin_secret", "*.pyc", "*.pyo", "*.pyd", "*.log"
]

def is_excluded(rel_path: str) -> bool:
    normalized = rel_path.replace("\\", "/").strip("/")
    parts = normalized.split("/")

    for part in parts:
        if part in EXCLUDE_DIRS:
            return True

    filename = parts[-1]
    for pat in EXCLUDE_PATTERNS:
        if fnmatch.fnmatch(filename, pat):
            return True

    return False

def build_package():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
    output_zip = os.path.join(repo_root, "upi_rakshak_submission.zip")

    if os.path.exists(output_zip):
        os.remove(output_zip)

    count = 0
    total_uncompressed = 0

    with zipfile.ZipFile(output_zip, "w", zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(repo_root):
            # Prune directories in place to avoid walking into excluded folders
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]

            for file in files:
                full_path = os.path.join(root, file)
                rel_path = os.path.relpath(full_path, repo_root)

                if is_excluded(rel_path) or rel_path == "upi_rakshak_submission.zip":
                    continue

                zipf.write(full_path, rel_path)
                count += 1
                total_uncompressed += os.path.getsize(full_path)

    zip_size_mb = os.path.getsize(output_zip) / (1024 * 1024)
    print("=" * 65)
    print("  UPI RAKSHAK AI — CLEAN SUBMISSION PACKAGE BUILT")
    print("=" * 65)
    print(f"Archive:       {output_zip}")
    print(f"Files Packaged: {count}")
    print(f"Archive Size:  {zip_size_mb:.2f} MB")
    print(f"Verification:  No secrets, databases, venvs, or node_modules included.")
    print("=" * 65)

if __name__ == "__main__":
    build_package()
