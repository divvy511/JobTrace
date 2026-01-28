import sqlite3
import config

def init_db():
    conn = sqlite3.connect(config.DATABASE_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS job_actions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        company TEXT,
        role TEXT,
        recruiter TEXT,
        action TEXT,
        channel TEXT,
        confidence REAL,
        timestamp TEXT
    )
    """)

    conn.commit()
    conn.close()
