#!/usr/bin/env python3
from json import load,dump
from sys import path as pathSys
from os import path as pathOs
from mail import send_mail
from threading import Thread
from time import sleep
from datetime import datetime, timedelta, timezone
from pprint import pprint

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import SEUILS, INTERVAL_DETECTIONS_MINUTES, TEMPS_INACTIVITE_MINUTES, CRISES_FILE
from DB_init import init, re_init
from log_manager import log_error

def load_crises():
    if pathOs.exists(CRISES_FILE):
        try:
            with open(CRISES_FILE, "r") as file:
                return load(file)
        except Exception as e:
            log_error(e)
    return {"seuils": {}, "inactives": {}}

def save_crises(data):
    try:
        with open(CRISES_FILE, "w") as file:
            dump(data, file)
    except Exception as e:
        log_error(e)

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

def critic(sonde,value):
    return sonde in SEUILS and value >= SEUILS[sonde]

def detector_crises():
    try:
        conn = init()
        if not conn:
            return

        crises = load_crises()
        already_alerted = crises["seuils"]

        while True:
            conn = re_init(conn)
            if not conn:
                return
            last_sonde_data = get_latest_sondes_datas(conn)

            for data in last_sonde_data:
                sonde,server,timestamp,value = data[1:]
                if server not in already_alerted and critic(sonde,value):
                    already_alerted[server] = [sonde]
                    send_mail("Alerte Crise!",f"Server '{server}':\nla sonde \"{sonde}\" à mesuré une valeur au dessus du seuil configuré ({SEUILS[sonde]}) le {timestamp}")
                elif server in already_alerted:
                    if sonde not in already_alerted[server] and critic(sonde,value):
                        already_alerted[server].append(sonde)
                        send_mail("Alerte Crise!",f"Server '{server}':\nla sonde \"{sonde}\" à mesuré une valeur au dessus du seuil configuré ({SEUILS[sonde]}) le {timestamp}")
                    elif sonde in already_alerted[server] and not critic(sonde,value):
                        already_alerted[server].remove(sonde)

            save_crises({"seuils": already_alerted, "inactives": crises["inactives"]})
            sleep(INTERVAL_DETECTIONS_MINUTES*60)
    except KeyboardInterrupt:
        pass
    except Exception as e:
        log_error(e)
    finally:
        if conn:
            conn.close()

def get_inactive_servers(conn):
    seuil_temps = (datetime.now(timezone.utc) - timedelta(minutes=TEMPS_INACTIVITE_MINUTES)).strftime('%Y-%m-%d %H:%M:%S')

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
    try:
        conn = init()
        if not conn:
            return

        crises = load_crises()
        already_alerted = set(crises["inactives"])

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
            
            save_crises({"seuils": crises["seuils"], "inactives": list(already_alerted)})
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