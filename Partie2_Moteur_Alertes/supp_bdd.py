import sqlite3
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATABASE_FILE

def delete(file,table,time,unit):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute(
        """
        DELETE FROM ?
        WHERE timestamp < NOW() - INTERVAL ? ?;
        """,
        (table,time,unit)
    )
    conn.commit()

if __name__ == '__main__':
    table = sys.argv[0] # ex: sonde_data
    time = sys.argv[1] # ex: 1
    unit = sys.argv[2] # ex: DAY
    delete(DATABASE_FILE,table,time,unit)