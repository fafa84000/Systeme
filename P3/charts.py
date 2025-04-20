from pygal import Line
from datetime import datetime
from sys import path as pathSys, argv
from os import path as pathOs

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from DB_init import init
from log_manager import log_error

def chart(server):
    conn = init()
    if not conn:
        return
    
    try:
        data = conn.execute(
            f"""
            SELECT sonde_name, timestamp, data
            FROM sonde_data
            WHERE server = ?
            ORDER BY timestamp ASC;
            """,
            (server,)
        ).fetchall()
    except Exception as e:
        log_error(e)
        return


    lineChart = Line(x_label_rotation=20, show_minor_x_labels=False)
    lineChart.title = f"Probes Data for Server: \"{server}\""

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
    lineChart.x_labels = [timestamp.strftime("%Y-%m-%d %H:%M") for timestamp in timestamps]
    lineChart.x_labels_major = lineChart.x_labels[::max(len(lineChart.x_labels)//10,1)]
    
    for sonde_name, sonde in sonde_data.items():
        values = [sonde["values"][sonde["timestamps"].index(timestamp)] if timestamp in sonde["timestamps"] else None for timestamp in timestamps]
        lineChart.add(sonde_name,values)

    lineChart.render_to_file('../line_chart.svg')


if __name__ == "__main__":
    server = argv[1]
    chart(server)