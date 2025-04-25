#!/usr/bin/env python3

from sys import path as pathSys
from os import path as pathOs
from datetime import datetime, timedelta, timezone

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import SUPRESSION_DONNEE_OBSOLETES_HOURS
from DB_init import init
from log_manager import log_error

def delete():
    conn = init()
    if not conn:
        return
    
    try:
        seuil_temps = (datetime.now(timezone.utc) - timedelta(minutes=SUPRESSION_DONNEE_OBSOLETES_HOURS)).strftime('%Y-%m-%d %H:%M:%S')

        conn.execute(
            f"""
            DELETE FROM sonde_data
            WHERE DATETIME(timestamp) < ?;
            """,
            (seuil_temps,)
        )
        conn.commit()
    except Exception as e:
        log_error(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    delete()