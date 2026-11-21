"""
Script to inspect verified user feedback from the SQLite database
and retrain/update the model when sufficient corrections have been gathered.
"""

import os
import sys
import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from backend.app.config import settings
from backend.app.models.db_models import Feedback
from backend.app.database import SessionLocal

def audit_and_export_feedback():
    db = SessionLocal()
    try:
        feedbacks = db.query(Feedback).all()
        print(f"Total user feedback entries collected: {len(feedbacks)}")
        
        incorrect_samples = [f for f in feedbacks if not f.is_correct and f.correct_category and f.input_text_masked]
        print(f"Actionable corrections with ground-truth re-labels: {len(incorrect_samples)}")
        
        if not incorrect_samples:
            print("No new verified corrections to incorporate into training dataset.")
            return False
            
        new_rows = []
        for f in incorrect_samples:
            new_rows.append({
                "template_id": f"feedback_{f.id}",
                "category": f.correct_category,
                "language": "en",
                "text": f.input_text_masked,
                "label": 0 if f.correct_category == "legitimate" else 1
            })
            
        data_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "data", "synthetic_scam_dataset.csv")
        df_existing = pd.read_csv(data_path)
        df_new = pd.DataFrame(new_rows)
        
        df_combined = pd.concat([df_existing, df_new], ignore_index=True)
        df_combined.drop_duplicates(subset=["text"], keep="last", inplace=True)
        df_combined.to_csv(data_path, index=False)
        print(f"Appended {len(new_rows)} user-corrected samples to {data_path}. Ready for retrain.")
        return True
    finally:
        db.close()

if __name__ == "__main__":
    audit_and_export_feedback()
