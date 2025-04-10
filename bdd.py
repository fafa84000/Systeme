import sqlite3
import json

DATABASE_FILE = 'monitoring.db'

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sonde_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sonde_name TEXT NOT NULL,
            server TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data TEXT NOT NULL
        )
        """
    )
    conn.commit()
    return conn

def store_sonde_data():
    # check photos (python socket)
    return

def clean_old_data(conn, retention_period_hours=24):
    c = conn.cursor()
    query = """
        DELETE FROM sonde_data
        WHERE timestamp < datetime('now', ?)
    """
    c.execute(query, (f'-{retention_period_hours} hours',))
    conn.commit()


if __name__ == "__main__":
    conn = init_db()
    
    conn.close()
