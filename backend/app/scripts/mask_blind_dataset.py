#!/usr/bin/env python3
"""
UPI Rakshak AI — Gold v3 PII Masking Utility
Sanitizes raw external smishing & alert submissions by stripping phone numbers,
account/card numbers, OTPs, personal names, and personal UPI VPAs.
"""

import sys
import json
import os
import argparse
import pandas as pd
from backend.app.core.masking import mask_blind_set_pii

def process_file(input_path: str, output_path: str):
    if not os.path.exists(input_path):
        print(f"[Error] Input file not found: {input_path}")
        sys.exit(1)

    print(f"Loading raw external dataset from: {input_path}")
    if input_path.endswith(".json"):
        with open(input_path, "r", encoding="utf-8") as f:
            records = json.load(f)
    elif input_path.endswith(".csv"):
        df = pd.read_csv(input_path)
        records = df.to_dict(orient="records")
    else:
        print("[Error] Unsupported file format. Use .json or .csv.")
        sys.exit(1)

    sanitized = []
    redaction_count = 0
    for idx, row in enumerate(records):
        raw_text = row.get("text", "")
        masked_text = mask_blind_set_pii(raw_text)
        if masked_text != raw_text:
            redaction_count += 1
        
        entry = dict(row)
        entry["text"] = masked_text
        entry["pii_masked"] = True
        sanitized.append(entry)

    print(f"Processed {len(records)} records. Redactions applied to {redaction_count} samples.")
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    if output_path.endswith(".json"):
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(sanitized, f, indent=2, ensure_ascii=False)
    elif output_path.endswith(".csv"):
        pd.DataFrame(sanitized).to_csv(output_path, index=False)

    print(f"Successfully saved sanitized blind set to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Mask PII in raw external evaluation datasets.")
    parser.add_argument("--input", "-i", required=True, help="Path to input raw JSON or CSV")
    parser.add_argument("--output", "-o", required=True, help="Path to output masked JSON or CSV")
    args = parser.parse_args()
    process_file(args.input, args.output)
