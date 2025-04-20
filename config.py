from sys import argv

HOST = "localhost"
PORT = 5000
SONDES_DIRECTORY = "C:/Users/assim/Documents/Univ/Systeme/P1"
# SONDES_DIRECTORY = "/home/uapv2306164/Systeme/P1"
FIND = "_sonde"
DATABASE_FILE = "C:/Users/assim/Documents/Univ/Systeme/monitoring.db"
# DATABASE_FILE = "/home/uapv2306164/Systeme/monitoring.db"
SQL = "C:/Users/assim/Documents/Univ/Systeme/monitoring.sql"
# SQL = "/home/uapv2306164/Systeme/monitoring.sql"

LOG_FILE = "C:/Users/assim/Documents/Univ/Systeme/error_log.txt"
# LOG_FILE = "/home/uapv2306164/Systeme/error_log.txt"

ALERTS_URL = "https://www.cert.ssi.gouv.fr/alerte/feed/"

#"nom_sonde" est le nom que la sonde envoie au port d'ecoute (PORT en haut de ce fichier); ex: "cpu"
# valeur est un entier ou un flotant que une sonde envoie; ex: 12.3
# syntaxe: "nom_sonde": valeur; ex: "cpu": 12.3, "users": 20
SEUILS = {
    "cpu": 0.0,
    "disk": 90.0,
    "users": 200
}

TEMPS_INACTIVITE_MINUTES = 30
INTERVAL_DETECTIONS_MINUTES = 60

if len(argv) > 1 and argv[1] == "print":
    print(f"{HOST} {PORT}")