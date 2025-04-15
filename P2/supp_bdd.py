import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_FILE

def delete(table,time,unit):
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    
    query = f"""
    DELETE FROM {table}
    WHERE timestamp < datetime('now', '-{time} {unit}');
    """
    c.execute(query)
    conn.commit()

if __name__ == '__main__':
    table = sys.argv[1] # ex: sonde_data
    time = sys.argv[2] # ex: 1
    unit = sys.argv[3] # ex: DAY
    delete(table,time,unit)