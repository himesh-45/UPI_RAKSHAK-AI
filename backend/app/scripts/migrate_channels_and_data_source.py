import os
import sqlite3
from backend.app.config import settings

def run_migration():
    db_url = settings.DATABASE_URL
    if "sqlite" not in db_url:
        print("[Migration] Non-sqlite database detected. Skipping local SQLite script.")
        return

    db_path = db_url.replace("sqlite:///", "")
    # Check both relative and backend/data paths
    paths = [db_path, "backend/data/upi_rakshak.db", "data/upi_rakshak.db"]
    target_paths = list(set([os.path.abspath(p) for p in paths if os.path.exists(p)]))

    if not target_paths:
        print(f"[Migration] No database file found to migrate among {paths}")
        return

    for path in target_paths:
        print(f"\n[Migration] Migrating database at: {path}")
        conn = sqlite3.connect(path)
        cur = conn.cursor()

        # 1. Ensure columns exist
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='analysis_history'")
        if not cur.fetchone():
            conn.close()
            continue

        cur.execute("PRAGMA table_info(analysis_history)")
        cols = [r[1] for r in cur.fetchall()]
        if "data_source" not in cols:
            cur.execute("ALTER TABLE analysis_history ADD COLUMN data_source VARCHAR(50) DEFAULT 'live_user'")
            conn.commit()

        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='threat_reports'")
        if cur.fetchone():
            cur.execute("PRAGMA table_info(threat_reports)")
            cols_tr = [r[1] for r in cur.fetchall()]
            if "data_source" not in cols_tr:
                cur.execute("ALTER TABLE threat_reports ADD COLUMN data_source VARCHAR(50) DEFAULT 'live_user'")
                conn.commit()

        # 2. Migrate WhatsApp records to legacy_removed and purge sender_hash
        cur.execute("SELECT COUNT(*) FROM analysis_history WHERE channel = 'whatsapp'")
        wa_count = cur.fetchone()[0]

        cur.execute("""
            UPDATE analysis_history
            SET channel = 'legacy_removed',
                sender_hash = NULL,
                data_source = 'test_traffic'
            WHERE channel = 'whatsapp'
        """)
        conn.commit()
        print(f"  -> Migrated {wa_count} WhatsApp records: channel='legacy_removed', sender_hash=NULL, data_source='test_traffic'")

        # 3. Tag demo seeds
        cur.execute("""
            UPDATE analysis_history
            SET data_source = 'demo_seed'
            WHERE is_simulated = 1 AND channel != 'legacy_removed'
        """)
        seed_count = cur.rowcount
        conn.commit()
        print(f"  -> Tagged {seed_count} demo seed records as data_source='demo_seed'")

        # 4. Tag test traffic in analysis_history
        test_patterns = [
            '%test%', '%sample%', '%benchmark%', '%judge%', '%mock%', '%pytest%',
            '%locust%', '%simulate%', '%temp%', '%load%'
        ]
        test_count = 0
        for pat in test_patterns:
            cur.execute("""
                UPDATE analysis_history
                SET data_source = 'test_traffic'
                WHERE (LOWER(raw_input_masked) LIKE ? OR sender_hash LIKE '%test%')
                  AND data_source NOT IN ('demo_seed', 'test_traffic')
            """, (pat,))
            test_count += cur.rowcount
            conn.commit()
        print(f"  -> Tagged {test_count} records as data_source='test_traffic'")

        # 5. Tag threat_reports
        cur.execute("""
            UPDATE threat_reports
            SET data_source = 'demo_seed'
            WHERE is_simulated = 1
        """)
        conn.commit()

        # Summary of final counts
        cur.execute("SELECT data_source, COUNT(*) FROM analysis_history GROUP BY data_source")
        summary = cur.fetchall()
        print("  -> Final AnalysisHistory data_source distribution:")
        for source, count in summary:
            print(f"     * {source}: {count}")

        cur.execute("SELECT channel, COUNT(*) FROM analysis_history GROUP BY channel")
        chan_summary = cur.fetchall()
        print("  -> Final AnalysisHistory channel distribution:")
        for chan, count in chan_summary:
            print(f"     * {chan}: {count}")

        conn.close()

if __name__ == "__main__":
    run_migration()
