import sys

HOST = "localhost"
PORT = 5000
PROBES_DIRECTORY = "/home/uapv2306164/Systeme/Partie1_Sondes"
FIND = "_sonde"
DATABASE_FILE = "/home/uapv2306164/Systeme/monitoring.db"
SQL = "/home/uapv2306164/Systeme/monitoring.sql"

if len(sys.argv) > 1:
    print(f"{HOST} {PORT}")
