import os
import re
import zipfile
import tempfile
import pytest

from backend.app.scripts.package_submission import build_package

FORBIDDEN_PATH_PATTERNS = [
    r'(?i)\.venv',
    r'(?i)\.git(?:[\\/]|$)',
    r'(?i)node_modules',
    r'(?i)\.pytest_cache',
    r'(?i)\.admin_secret',
    r'(?i)\.env(?:\.local)?$',
    r'(?i)\.(?:db|sqlite|sqlite3)$',
]

LOCAL_ABSOLUTE_PATH_REGEX = re.compile(
    r'(?i)(?:[a-zA-Z]:\\(?:users|documents|appdata)|file:///[a-zA-Z]:/|(?:^|[\s\'"\(])/(?:Users|home)/[a-zA-Z0-9_\-]+/)'
)

TEXT_FILE_EXTENSIONS = {
    ".py", ".md", ".json", ".js", ".jsx", ".ts", ".tsx", ".html", ".css", ".yaml", ".yml", ".txt", ".sh"
}

def test_submission_package_integrity():
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    zip_path = os.path.join(repo_root, "upi_rakshak_submission.zip")

    # Build fresh package
    build_package()
    assert os.path.exists(zip_path), f"Package zip not generated at {zip_path}"

    with tempfile.TemporaryDirectory() as tmpdir:
        with zipfile.ZipFile(zip_path, "r") as zf:
            namelist = zf.namelist()
            assert len(namelist) >= 50, f"Expected at least 50 files in submission, got {len(namelist)}"

            # 1. Check for forbidden file and folder patterns in zip member names
            for name in namelist:
                for pat in FORBIDDEN_PATH_PATTERNS:
                    assert not re.search(pat, name), f"Forbidden artifact pattern '{pat}' matched inside zip member: {name}"

            # Extract archive to verify contents
            zf.extractall(tmpdir)

        # 2. Verify extracted tree has no database files, secrets, or forbidden dirs
        for root, dirs, files in os.walk(tmpdir):
            for d in dirs:
                assert d not in {".venv", ".git", "node_modules", ".pytest_cache", "__pycache__"}, f"Forbidden dir found: {d}"
            for f in files:
                assert not f.endswith((".db", ".sqlite", ".sqlite3")), f"Database file found: {f}"
                assert f not in {".env", ".env.local", ".admin_secret"}, f"Secret file found: {f}"

        # 3. Check for absolute local machine paths inside text files
        flagged_paths = []
        for root, dirs, files in os.walk(tmpdir):
            for f in files:
                ext = os.path.splitext(f)[1].lower()
                if ext in TEXT_FILE_EXTENSIONS:
                    file_path = os.path.join(root, f)
                    try:
                        with open(file_path, "r", encoding="utf-8", errors="ignore") as content_file:
                            for line_idx, line in enumerate(content_file, 1):
                                if line.strip().startswith(("http://", "https://")):
                                    continue
                                matches = LOCAL_ABSOLUTE_PATH_REGEX.findall(line)
                                if matches:
                                    rel = os.path.relpath(file_path, tmpdir)
                                    flagged_paths.append((rel, line_idx, matches[:3]))
                    except Exception:
                        pass

        assert len(flagged_paths) == 0, f"Absolute local paths found in packaged files: {flagged_paths}"

        # 4. Check that core files are present
        assert os.path.exists(os.path.join(tmpdir, "backend", "app", "main.py"))
        assert os.path.exists(os.path.join(tmpdir, "frontend", "src", "App.jsx"))
        assert os.path.exists(os.path.join(tmpdir, "Makefile"))
        assert os.path.exists(os.path.join(tmpdir, "README.md"))
        assert os.path.exists(os.path.join(tmpdir, "docs", "EVALUATION_REPORT.md"))
