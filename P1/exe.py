#!/usr/bin/env python3

import importlib.util
from sys import path as pathSys
from os import path as pathOs, listdir
from subprocess import run
from socket import socket, gethostname
from time import sleep

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import HOST, PORT, SONDES_DIRECTORY, FIND, INTERVAL_RECUPERATION_DONNEE_SONDES_SECONDS
from log_manager import log_error

def get_data_py(sonde):
    spec = importlib.util.spec_from_file_location("sonde_module", sonde)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    if hasattr(module, "data"):
        return module.data()
    return None

def get_data_sh(sonde):
    try:
        result = run([sonde], capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except Exception as e:
        log_error(e)
        return None

def get_data(sonde):
    if sonde.endswith('.py'):
        return get_data_py(sonde)
    else:
        return get_data_sh(sonde)

def send_message(message):
    try:
        client_socket = socket()
        client_socket.connect((HOST, PORT))
        client_socket.send(message.encode())
        client_socket.close()
    except Exception as e:
        log_error(e)

def main():
    sleep(2)
    
    try:
        send_message("update sondes number")
        fichiers = listdir(SONDES_DIRECTORY)
        sondes = [f for f in fichiers if f.endswith(f'{FIND}.py') or f.endswith(f'{FIND}.sh')]
        print(f"Sondes presentes dans le dossier \"{SONDES_DIRECTORY}\":")
        for sonde in sondes:
            print(f"\t- {sonde}")
        datas = {}
        for sonde in sondes:
            sonde_path = pathOs.join(SONDES_DIRECTORY, sonde)
            sonde_name = sonde[:-9]
            datas[sonde_name] = get_data(sonde_path)
            print(f"Execution: {sonde_name}, data: {datas[sonde_name]}")
        for data in datas:
            send_message(f"sonde\t{gethostname()}\t{data}\t{datas[data]}")
    except Exception as e:
        log_error(e)

if __name__ == "__main__":
    main()
