from flask import Flask, render_template, url_for
from sys import path as pathSys
from os import path as pathOs, listdir

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import CHART_FOLDER
from DB_init import init

app = Flask(__name__)

def get_alerts():
    conn = init()
    if not conn:
        return
    
    try:
        return conn.execute("SELECT * FROM alertes;").fetchall()
    except Exception as e:
        return []

@app.route('/')
def index():
    files = [f for f in listdir(CHART_FOLDER) if f.endswith('.svg')]
    servers = set()
    for filename in files:
        name = filename[:-4]
        server_name = name.split('_')[0]
        servers.add(server_name)
    servers = sorted(servers)

    alertes = get_alerts()

    return render_template('index.html', servers=servers, alertes=alertes)

@app.route('/details/<server_name>')
def details(server_name):
    detail_files = [f for f in listdir(CHART_FOLDER) if f.startswith(server_name+'_') and f.endswith('.svg')]
    detail_files.sort()
    charts = [
        {
            'file': f,
            'label': f[len(server_name)+1:-4]
        }
        for f in detail_files
    ]
    return render_template('details.html', server_name=server_name, charts=charts)

if __name__ == '__main__':
    app.run(debug=False, port=8080)