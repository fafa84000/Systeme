import os
import time
import subprocess
import socket
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOST, PORT, PROBES_DIRECTORY, FIND

def executer_sonde(sonde):
    try:
        if sonde.endswith('.py'):
            subprocess.run(['python', sonde], check=True)
        elif sonde.endswith('.sh'):
            subprocess.run(['bash', sonde], check=True)
        print(f"Sonde {sonde} exécutée avec succès.")
    except subprocess.CalledProcessError as e:
        print(f"Erreur lors de l'exécution de {sonde}: {e}")

def main():
    client_socket = socket.socket()
    client_socket.connect((HOST, PORT))

    message = "update sondes number"
    client_socket.send(message.encode())

    client_socket.close()
    
    fichiers = os.listdir(PROBES_DIRECTORY)

    sondes = [f for f in fichiers if f.endswith(f'{FIND}.py') or f.endswith(f'{FIND}.sh')]

    if not sondes:
        print("Aucune sonde trouvée dans le dossier.")
    else:
        print("Sondes trouvées :")
        for sonde in sondes:
            print(f"- {sonde}")

    for sonde in sondes:
        sonde_path = os.path.join(PROBES_DIRECTORY, sonde)
        executer_sonde(sonde_path)
        time.sleep(5)

if __name__ == "__main__":
    main()
