from pygal import Line
from datetime import datetime, timezone, timedelta
from sys import path as pathSys
from os import path as pathOs
from subprocess import run
from time import sleep
from argparse import ArgumentParser, ArgumentTypeError

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import CHART_FOLDER, INTERVAL_RECUPERATION_DONNEE_SONDES_SECONDS
from DB_init import init
from log_manager import log_error

def parse_timestamp(timestamp):
    try:
        input_timestamp = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S")

        current_utc_time = datetime.now(timezone.utc).replace(tzinfo=None)

        if input_timestamp > current_utc_time:
            raise ValueError("The provided timestamp is in the future. Please provide a UTC tiem in the past")
        
        return input_timestamp
    except ValueError:
        log_error(e)
        raise ArgumentTypeError(
            f"Invalid timestamp format: '{timestamp}'. Expected format: YYYY-MM-DD HH:MM:SS"
        )
    except Exception as e:
        log_error(e)

def get_args():
    parser = ArgumentParser(description="Process server and sondes options.")
    parser.add_argument(
        "-servers",
        nargs="+",
        type=str,
        default=None,
        help="Specify the server names. \"... -server ServerName1 ServerName2 ServerNameEct... ...\""
    )
    parser.add_argument(
        "-sondes",
        nargs="+",
        type=str,
        default=None,
        help="Specify sondes names. \"... -sondes SondeName1 SondeName2 SondeNameEct... ...\""
    )
    parser.add_argument(
        "-after",
        type=parse_timestamp,
        default=parse_timestamp("0001-01-01 00:00:00"),
        help="Specify timestamp to get data after it. \"... -after YYYY-mm-dd H:M:S ...\""
    )
    args = parser.parse_args()
    return args.servers,args.sondes,args.after

def generate_chart(conn,file_name,title,server, sondes, after):    
    try:
        sondes_str = "( "
        for sonde in sondes:
            sondes_str += "sonde_name = '" + sonde + "' or "
        sondes_str = sondes_str[:-3] + ")"
        data = conn.execute(
            f"""
            SELECT sonde_name, timestamp, data
            FROM sonde_data
            WHERE server = ? and {sondes_str} and DATETIME(timestamp) > ?
            ORDER BY timestamp ASC;
            """,
            (server,after)
        ).fetchall()
    except Exception as e:
        log_error(e)
        return

    if '_' in file_name:
        lineChart = Line(show_x_labels=False)
    else:
        lineChart = Line(show_minor_x_labels=False)
    lineChart.title = title

    if not data:
        lineChart.add("No Data",[])
        lineChart.render_to_file('line_chart.svg')
        return
    
    sonde_data = {}
    for sonde_name, timestamp, value in data:
        if sonde_name not in sonde_data:
            sonde_data[sonde_name] = {"timestamps": [], "values": []}
        sonde_data[sonde_name]["timestamps"].append(datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S"))
        sonde_data[sonde_name]["values"].append(value)
    
    timestamps = sorted({timestamp for sonde in sonde_data.values() for timestamp in sonde["timestamps"]})
    lineChart.x_labels = [timestamp.strftime("%H:%M") for timestamp in timestamps]
    # lineChart.x_labels_major = lineChart.x_labels[::max(len(lineChart.x_labels)//10,1)]
    lineChart.x_labels_major = labels = ["-00:0" + str(i) if i < 10 else "-00:" + str(i) for i in range(30, 0, -2)]
    
    for sonde_name, sonde in sonde_data.items():
        values = [sonde["values"][sonde["timestamps"].index(timestamp)] if timestamp in sonde["timestamps"] else None for timestamp in timestamps]
        lineChart.add(sonde_name,values)

    lineChart.render_to_file(CHART_FOLDER+file_name)

def get_all_servers_names(conn):
    try:
        result = conn.execute(
            """
            SELECT DISTINCT server
            FROM sonde_data;
            """
        ).fetchall()
        servers = []
        for server in result:
            servers.append(server[0])
        return servers
    except Exception as e:
        log_error(e)
        return []

def get_sondes_names(conn,server):
    try:
        result = conn.execute(
            """
            SELECT DISTINCT sonde_name
            FROM sonde_data
            WHERE server = ?;
            """,
            (server,)
        ).fetchall()
        sondes = []
        for sonde in result:
            sondes.append(sonde[0])
        return sondes
    except Exception as e:
        log_error(e)
        return []

def empty_dir(servers):
    exclude_pattern = "! -name '*" + "' ! -name '*".join(servers) + "'"

    # Commande bash
    command = f"find {CHART_FOLDER} -type f {exclude_pattern} -delete"

    # Exécution de la commande
    run(["bash", "-c", command])


def charts(servers,sondes,after):
    sleep(5)

    conn = init()
    if not conn:
        return

    if not servers:
        servers = get_all_servers_names(conn)

    empty_dir(servers)

    for server in servers:
        if not sondes:
            sondes = get_sondes_names(conn,server)

        if len(sondes) > 1:
            derniere_heure = (datetime.now(timezone.utc) - timedelta(minutes=30)).strftime("%Y-%m-%d %H:%M:%S")
            generate_chart(conn,server+".svg",f"Données en Live des sondes du serveur \"{server}\"\nau cours de la dernière demi-heure (MáJ toutes les 2 minutes)",server,sondes,derniere_heure)

        for sonde in sondes:
            generate_chart(conn,server+"_"+sonde+".svg",f"Données historiques en Live pour la sonde \"{sonde}\" (MáJ toutes les 2 minutes)",server,[sonde],after)


if __name__ == "__main__":
    servers, sondes, after = get_args()
    charts(servers,sondes,after)