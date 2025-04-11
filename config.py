import sys

HOST = "localhost"
PORT = 5000
PROBES_DIRECTORY = "~/Systeme/Partie1_Sondes"
FIND = "_sonde"
DATABASE_FILE = "~/Systeme/monitoring.db"
SQL = "~/Systeme/monitoring.sql"

if len(sys.argv) > 1:
    print(f"{HOST} {PORT}")