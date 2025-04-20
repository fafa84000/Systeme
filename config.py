from sys import argv

# PROJECT_ROOT = "C:/Users/assim/Documents/Univ/Systeme/"
# PROJECT_ROOT = "/home/uapv2306164/Systeme/"
PROJECT_ROOT = "/home/lsfaj/Systeme/"

HOST = "localhost"
PORT = 5000
SONDES_DIRECTORY = PROJECT_ROOT + "P1"
FIND = "_sonde"
DATABASE_FILE = PROJECT_ROOT + "monitoring.db"
SQL = PROJECT_ROOT + "monitoring.sql"

LOG_FILE = PROJECT_ROOT + "log.log"

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