import os
import zipfile
import pytest
from backend.app.scripts.package_submission import build_package, is_excluded

def test_is_excluded_filters_secrets():
    assert is_excluded("backend/data/.admin_secret") is True
    assert is_excluded(".env") is True
    assert is_excluded("backend/.env.local") is True
    assert is_excluded("data/upi_rakshak.db") is True
    assert is_excluded(".venv/Lib/site-packages/something.py") is True
    assert is_excluded("frontend/node_modules/vite/index.js") is True
    assert is_excluded(".git/config") is True

    # Should not exclude genuine source code
    assert is_excluded("backend/app/main.py") is False
    assert is_excluded("frontend/src/App.jsx") is False
    assert is_excluded("docs/EVALUATION_REPORT.md") is False


def test_package_submission_creates_clean_zip(tmp_path):
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    zip_path = os.path.join(repo_root, "upi_rakshak_submission.zip")
    
    # Run packaging
    build_package()
    assert os.path.exists(zip_path), "Submission zip was not created"
    
    # Inspect zip contents
    with zipfile.ZipFile(zip_path, "r") as zf:
        namelist = zf.namelist()
        assert len(namelist) > 50, "Zip archive should contain codebase files"
        
        for name in namelist:
            parts = name.replace("\\", "/").split("/")
            assert not name.endswith(".db"), f"Forbidden db file in zip: {name}"
            assert not name.endswith(".admin_secret"), f"Forbidden secret file in zip: {name}"
            assert not name.endswith(".env"), f"Forbidden .env in zip: {name}"
            assert "node_modules" not in parts, f"node_modules found in zip: {name}"
            assert ".venv" not in parts, f".venv found in zip: {name}"
            assert ".git" not in parts, f".git directory found in zip: {name}"
