import os
import zipfile
import io
import requests
import pandas as pd
from typing import Dict, Any

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "external")

def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)

def download_uci_sms_spam() -> str:
    """
    Downloads the UCI SMS Spam Collection.
    License: Creative Commons Attribution 4.0 International (CC BY 4.0) / Public Domain.
    """
    out_file = os.path.join(DATA_DIR, "sms_spam_collection.csv")
    if os.path.exists(out_file):
        print(f"[UCI SMS] Already exists at {out_file}")
        return out_file

    url_zip = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
    url_mirror = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"

    print(f"[UCI SMS] Fetching from {url_zip} ...")
    try:
        resp = requests.get(url_zip, timeout=15)
        if resp.status_code == 200:
            with zipfile.ZipFile(io.BytesIO(resp.content)) as z:
                with z.open("SMSSpamCollection") as f:
                    lines = f.read().decode("utf-8", errors="ignore").splitlines()
                    rows = []
                    for line in lines:
                        parts = line.split("\t", 1)
                        if len(parts) == 2:
                            label, text = parts
                            rows.append({"label": label.strip(), "text": text.strip(), "source": "uci_sms_collection"})
                    df = pd.DataFrame(rows)
                    df.to_csv(out_file, index=False)
                    print(f"[UCI SMS] Successfully parsed {len(df)} messages to {out_file}")
                    return out_file
    except Exception as e:
        print(f"[UCI SMS] Primary zip download failed: {e}. Trying mirror...")

    try:
        resp = requests.get(url_mirror, timeout=15)
        if resp.status_code == 200:
            lines = resp.text.splitlines()
            rows = []
            for line in lines:
                parts = line.split("\t", 1)
                if len(parts) == 2:
                    label, text = parts
                    rows.append({"label": label.strip(), "text": text.strip(), "source": "uci_sms_collection"})
            df = pd.DataFrame(rows)
            df.to_csv(out_file, index=False)
            print(f"[UCI SMS] Successfully parsed {len(df)} messages from mirror to {out_file}")
            return out_file
    except Exception as e:
        print(f"[UCI SMS] Mirror download also failed: {e}")

    return ""

def download_openphish_feed() -> str:
    """
    Downloads active phishing URLs from OpenPhish free community feed.
    """
    out_file = os.path.join(DATA_DIR, "openphish_feed.txt")
    url = "https://openphish.com/feed.txt"
    print(f"[OpenPhish] Fetching active feed from {url} ...")
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(resp.text)
            url_count = len([l for l in resp.text.splitlines() if l.strip()])
            print(f"[OpenPhish] Downloaded {url_count} active phishing URLs to {out_file}")
            return out_file
        else:
            print(f"[OpenPhish] Received status code {resp.status_code}")
    except Exception as e:
        print(f"[OpenPhish] Download failed: {e}")
    return ""

def download_tranco_benign_domains() -> str:
    """
    Downloads a sample of top benign domains from Tranco or a curated benign domains feed.
    """
    out_file = os.path.join(DATA_DIR, "benign_domains.csv")
    if os.path.exists(out_file):
        print(f"[Benign Domains] Already exists at {out_file}")
        return out_file

    url = "https://raw.githubusercontent.com/datasets/top-1000-websites/master/data/top-1000-websites.csv"
    print(f"[Benign Domains] Fetching from {url} ...")
    try:
        resp = requests.get(url, timeout=15)
        if resp.status_code == 200:
            with open(out_file, "w", encoding="utf-8") as f:
                f.write(resp.text)
            print(f"[Benign Domains] Downloaded benign domains list to {out_file}")
            return out_file
    except Exception as e:
        print(f"[Benign Domains] Download failed: {e}")
    return ""

def main():
    ensure_data_dir()
    sms_path = download_uci_sms_spam()
    phish_path = download_openphish_feed()
    benign_path = download_tranco_benign_domains()
    print("Download public data completed.")

if __name__ == "__main__":
    main()
