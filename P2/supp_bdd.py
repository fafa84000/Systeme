#!/usr/bin/env python3

from sys import path as pathSys, argv
from os import path as pathOs

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from DB_init import init
from log_manager import log_error

def delete(table,time,unit):
    conn = init()
    if not conn:
        return
    
    try:
        conn.execute(
            f"""
            DELETE FROM {table}
            WHERE timestamp < datetime('now', '-{time} {unit}');
            """
        )
    except Exception as e:
        log_error(e)
    finally:
        if conn:
            conn.close()

if __name__ == '__main__':
    table = argv[1] # ex: sonde_data
    time = argv[2] # ex: 1
    unit = argv[3] # ex: DAY
    delete(table,time,unit)