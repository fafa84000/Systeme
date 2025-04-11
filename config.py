import sys

HOST = "localhost"
PORT = 5000
PROBES_DIRECTORY = "../Partie1_Sondes"
FIND = "_sonde"
DATABASE_FILE = "../monitoring.db"
SQL = "../monitoring.sql"

if len(sys.argv) > 1:
    print(f"{HOST} {PORT}")