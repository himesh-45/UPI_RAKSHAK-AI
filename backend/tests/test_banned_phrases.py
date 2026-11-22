import os
import re
import pytest

BANNED_PATTERNS = [
    re.compile(r'(?i)\bbulletproof\b'),
    re.compile(r'(?i)\bproduction[- ]ready\b'),
    re.compile(r'(?i)\bimmune to\b'),
    re.compile(r'(?i)\b100%\s+accuracy\b'),
    re.compile(r'(?i)\b100%\s+accurate\b'),
    re.compile(r'(?i)\bzero\s+false\s+positive\b'),
    re.compile(r'(?i)\bzero\s+hallucination\b'),
    re.compile(r'(?i)\bguaranteed\s+safe\b'),
]

SCAN_EXTENSIONS = ('.md', '.py', '.jsx', '.js', '.html')
IGNORE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', 'dist', '.pytest_cache'}

def get_files_to_scan():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files_to_scan = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f.endswith(SCAN_EXTENSIONS) and f != "test_banned_phrases.py":
                files_to_scan.append(os.path.join(root, f))
    return files_to_scan

def test_no_banned_absolute_claims():
    files = get_files_to_scan()
    violations = []

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                # Ignore lines that explicitly cite banned words as test assertions or disclaimers
                if "BANNED" in line or "never claim" in line.lower() or "not a guarantee" in line.lower():
                    continue
                for pat in BANNED_PATTERNS:
                    if pat.search(line):
                        rel_path = os.path.relpath(fpath)
                        violations.append(f"{rel_path}:{line_no} matches '{pat.pattern}': {line.strip()[:100]}")

    assert not violations, f"Found absolute/unsupported claims in codebase:\n" + "\n".join(violations[:20])
