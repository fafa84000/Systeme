#!/usr/bin/env python3

from sys import path as pathSys
from os import path as pathOs, listdir
from time import sleep
from subprocess import run
from socket import socket

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import HOST, PORT, SONDES_DIRECTORY, FIND
from log_manager import log_error

def executer_sonde(sonde):
    try:
        if sonde.endswith('.py'):
            run(['python3', sonde], check=True)
        elif sonde.endswith('.sh'):
            run(['bash', sonde], check=True)
    except Exception as e:
        log_error(e)

def main():
    try:
        client_socket = socket()
        client_socket.connect((HOST, PORT))

        message = "update sondes number"
        client_socket.send(message.encode())

        client_socket.close()
    except Exception as e:
        log_error(e)
    
    try:
        fichiers = listdir(SONDES_DIRECTORY)
        sondes = [f for f in fichiers if f.endswith(f'{FIND}.py') or f.endswith(f'{FIND}.sh')]
        print(f"Sondes presentes dans le dossier \"{SONDES_DIRECTORY}\":")
        for sonde in sondes:
            print(f"\t- {sonde}")
        print("\n")
        for sonde in sondes:
            sonde_path = pathOs.join(SONDES_DIRECTORY, sonde)
            executer_sonde(sonde_path)
            print(f"Execution: {sonde}")
            sleep(5)
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    main()
