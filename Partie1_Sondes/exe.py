import os
import time
import subprocess

dossier_sondes = './'

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
    fichiers = os.listdir(dossier_sondes)

    sondes = [f for f in fichiers if f.endswith('_sonde.py') or f.endswith('_sonde.sh')]

    if not sondes:
        print("Aucune sonde trouvée dans le dossier.")
    else:
        print("Sondes trouvées :")
        for sonde in sondes:
            print(f"- {sonde}")

    for sonde in sondes:
        sonde_path = os.path.join(dossier_sondes, sonde)
        executer_sonde(sonde_path)
        time.sleep(5)

if __name__ == "__main__":
    main()
