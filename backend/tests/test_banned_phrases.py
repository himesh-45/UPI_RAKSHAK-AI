import os
import re
import pytest

BANNED_PATTERNS = [
    re.compile(r'(?i)\bbulletproof\b'),
    re.compile(r'(?i)\bproduction[- ]ready\b'),
    re.compile(r'(?i)\bimmune\s+to\b'),
    re.compile(r'(?i)\b100%\s+accuracy\b'),
    re.compile(r'(?i)\b100%\s+accurate\b'),
    re.compile(r'(?i)\bzero\s+false\s+positives?\b'),
    re.compile(r'(?i)\bzero\s+false\s+alarm\b'),
    re.compile(r'(?i)\bzero\s+hallucination\b'),
    re.compile(r'(?i)\bguaranteed\s+safe\b'),
    re.compile(r'(?i)\bzero\s+fabricated\s+metrics\b'),
    re.compile(r'(?i)\b100%\s+programmatically\b'),
    re.compile(r'(?i)\b100%\s+offline\b'),
    re.compile(r'(?i)\bzero\s+secrets\b'),
    re.compile(r'(?i)\bsub-20ms\b'),
    re.compile(r'(?i)\b12ms\b'),
    re.compile(r'(?i)\b100%\s+native\b'),
    re.compile(r'(?i)\bzero\s+external\s+pip\s+dependencies\b'),
]

SCAN_EXTENSIONS = ('.md', '.py', '.jsx', '.js', '.html')
IGNORE_DIRS = {'.git', '.venv', 'node_modules', '__pycache__', 'dist', '.pytest_cache'}

def get_files_to_scan():
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    files_to_scan = []
    for root, dirs, files in os.walk(base_dir):
        dirs[:] = [d for d in dirs if d not in IGNORE_DIRS]
        for f in files:
            if f == "test_banned_phrases.py":
                continue
            # Scan standard code/doc extensions and frontend i18n JSON files
            if f.endswith(SCAN_EXTENSIONS) or (f.endswith('.json') and 'i18n' in root):
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


BANNED_WHATSAPP_PATTERNS = [
    re.compile(r'(?i)\bwhatsapp\s+bot\b'),
    re.compile(r'(?i)\bwhatsapp_webhook\b'),
    re.compile(r'\bWHATSAPP_[A-Z0-9_]+'),
]


def test_no_whatsapp_bot_reintroduction():
    files = get_files_to_scan()
    violations = []

    for fpath in files:
        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
            for line_no, line in enumerate(f, 1):
                if "BANNED" in line or "never claim" in line.lower() or "legacy_removed" in line:
                    continue
                for pat in BANNED_WHATSAPP_PATTERNS:
                    if pat.search(line):
                        rel_path = os.path.relpath(fpath)
                        violations.append(f"{rel_path}:{line_no} matches '{pat.pattern}': {line.strip()[:100]}")

    assert not violations, f"Found prohibited WhatsApp Bot or webhook references in codebase:\n" + "\n".join(violations[:20])

