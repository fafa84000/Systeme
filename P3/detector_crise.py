#!/usr/bin/env python3

from sys import path as pathSys
from os import path as pathOs
from mail import send_mail
from threading import Thread
from time import sleep
from datetime import datetime, timedelta

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import SEUILS, INTERVAL_DETECTIONS_MINUTES, TEMPS_INACTIVITE_MINUTES
from DB_init import init, re_init
from log_manager import log_error

def get_latest_sondes_datas(conn):
    try:
        return conn.execute(
            """
            SELECT sd.*
            FROM sonde_data sd
            JOIN (
                SELECT sonde_name, server, MAX(timestamp) AS timestamp
                FROM sonde_data
                GROUP BY sonde_name, server
            ) latest ON
            sd.sonde_name = latest.sonde_name 
            AND
            sd.server = latest.server 
            AND
            sd.timestamp = latest.timestamp;
            """
        ).fetchall()
    except Exception as e:
        log_error(e)
        return []

def critic(data):
    return data[1] in SEUILS and data[4] >= SEUILS[data[1]]

def detector_crises():
    conn = init()
    if not conn:
        return

    already_alerted = {}

    try:
        while True:
            conn = re_init(conn)
            if not conn:
                return
            last_sonde_data = get_latest_sondes_datas(conn)

            for data in last_sonde_data:
                if data[2] not in already_alerted and critic(data): # server not alerted and critic data -> send alert
                    already_alerted[data[2]] = [data[1]]
                    send_mail("Alerte Crise!",f"Server '{data[2]}':\nla sonde \"{data[1]}\" à mesuré une valeur au dessus du seuil configuré ({SEUILS[data[1]]}) le {data[3]}")
                elif data[2] in already_alerted:
                    if data[1] not in already_alerted[data[2]] and critic(data): # server alerted but data not present in the already alerted data -> send alert
                        already_alerted[data[2]].append(data[1])
                        send_mail("Alerte Crise!",f"Server '{data[2]}':\nla sonde \"{data[1]}\" à mesuré une valeur au dessus du seuil configuré ({SEUILS[data[1]]}) le {data[3]}")
                    elif data[1] in already_alerted[data[2]] and not critic(data): # server alerted but current data no more critic -> remove alert
                        already_alerted[data[2]].remove(data[1])

            sleep(INTERVAL_DETECTIONS_MINUTES*60)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log_error(e)
    finally:
        if conn:
            conn.close()

def get_inactive_servers(conn):
    seuil_temps = (datetime.now() - timedelta(minutes=TEMPS_INACTIVITE_MINUTES)).strftime('%Y-%m-%d %H:%M:%S')

    try:
        return conn.execute(
            """
            SELECT server, MAX(timestamp) AS timestamp
            FROM sonde_data
            GROUP BY server
            HAVING DATETIME(timestamp) < ?;
            """,
            (seuil_temps,)
        ).fetchall()
    except Exception as e:
        log_error(e)
        return []

def detector_inactivity():
    conn = init()
    if not conn:
        return

    already_alerted = set()

    try:
        while True:
            conn = re_init(conn)
            if not conn:
                return
            inactive_servers = get_inactive_servers(conn)
            current_inactive = set(server for server, _ in inactive_servers)

            new_alerts = current_inactive - already_alerted

            if new_alerts:
                for server in new_alerts:
                    send_mail("Inactivité",f"Le serveur {server} est inactif.")
                already_alerted.update(new_alerts)
            
            resolved_alerts = already_alerted - current_inactive
            if resolved_alerts:
                already_alerted -= resolved_alerts
            
            sleep(INTERVAL_DETECTIONS_MINUTES*60)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log_error(e)
    finally:
        if conn:
            conn.close()
        
if __name__ == '__main__':
    try:
        Thread(target=detector_crises).start()
        Thread(target=detector_inactivity).start()
    except Exception as e:
        log_error(e)