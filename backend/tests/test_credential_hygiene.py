import os
import subprocess
import pytest

def test_no_hardcoded_admin_credentials_in_repo():
    """
    Grep the entire repository for known demo password patterns and assert none exist in tracked files.
    Fails if legacy hardcoded passwords are found in any codebase file or documentation.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    forbidden = "Admin" + "Rakshak"
    
    # Use git grep to search tracked files
    res = subprocess.run(
        ["git", "grep", "-I", "-i", forbidden, ":(exclude)backend/tests/*"],
        cwd=repo_root,
        capture_output=True,
        text=True
    )
    
    assert res.returncode != 0, f"Found hardcoded admin credentials in repo:\n{res.stdout}"


def test_i18n_has_no_demo_credentials_notice():
    """
    Asserts demoCredentialsNotice is removed from all frontend i18n JSON files.
    """
    repo_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    i18n_dir = os.path.join(repo_root, "frontend", "src", "i18n")
    forbidden = "Admin" + "Rakshak"
    
    if os.path.exists(i18n_dir):
        for f in os.listdir(i18n_dir):
            if f.endswith(".json"):
                path = os.path.join(i18n_dir, f)
                with open(path, "r", encoding="utf-8") as fp:
                    content = fp.read()
                    assert "demoCredentialsNotice" not in content, f"demoCredentialsNotice found in {f}"
                    assert forbidden not in content, f"Hardcoded credential found in {f}"
