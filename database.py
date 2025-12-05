import sqlite3
from pathlib import Path

DB_PATH = Path("vehicles.db")

def init_db():
    """Initialize the database and create vehicles table if it doesn't exist."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS vehicles (
            vin TEXT PRIMARY KEY,
            manufacturer TEXT NOT NULL,
            description TEXT,
            horse_power INTEGER NOT NULL,
            model_name TEXT NOT NULL,
            model_year INTEGER NOT NULL,
            purchase_price REAL NOT NULL,
            fuel_type TEXT NOT NULL
        )
    """)
    conn.commit()
    conn.close()

def get_db():
    """SQLite connection dependency for FastAPI."""
    conn = sqlite3.connect(DB_PATH)
    try:
        yield conn
    finally:
        conn.close()
