#!/usr/bin/env python3

from socket import socket
from sys import path as pathSys
from os import path as pathOs, listdir
from pprint import pprint

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import HOST, PORT, SONDES_DIRECTORY, FIND
from DB_init import init, re_init
from log_manager import log_error

def store_data_in_db(conn, sonde_name, server, data):
    try:
        conn.execute(
            """
            INSERT INTO sonde_data (sonde_name, server, data)
            VALUES (?, ?, ?)
            """,
            (sonde_name, server, data)
        )
        print("Sonde stockée")
    except Exception as e:
        log_error(e)
        pprint(e)

def store_alerte_in_db(conn, title, link, description):
    try:
        conn.execute(
            """
            INSERT INTO alertes (title, link, description)
            SELECT ?, ?, ?
            WHERE NOT EXISTS (
                SELECT 1 FROM alertes WHERE link = ?
            );
            """,
            (title, link, description, link)
        )
        print("Alerte stockée")
    except Exception as e:
        log_error(e)
        pprint(e)

def count_files_in_directory():
    return len([f for f in listdir(SONDES_DIRECTORY) if '.' in f and f.split('.')[-2].endswith(FIND)])

def run_server():
    conn = init()
    if not conn:
        return

    try:
        server_socket = socket()
        server_socket.bind((HOST, PORT))
        print(f"Port {PORT} ouvert !")
    except Exception as e:
        log_error(e)
        pprint(e)
        return

    try:
        while True:
            conn = re_init(conn)
            if not conn:
                return
            num_files = count_files_in_directory()
            server_socket.listen(num_files)
            print(f"{num_files} fichiers en ecoute.")

            client_socket = server_socket.accept()[0]

            data = client_socket.recv(1024).decode('utf-8')
            print(f"Donnée reçue:\n\t\t{data}\n")
            if data:
                if data[0] == "u":
                    continue
                elif data[0] == "s":
                    try:
                        server, sonde_name, sonde_data = data.split('\t')[1:]
                        store_data_in_db(conn, sonde_name, server, sonde_data)
                    except Exception as e:
                        log_error(e)
                        pprint(e)
                elif data[0] == "a":
                    try:
                        title,link,description = data.split('\t')[1:]
                        store_alerte_in_db(conn,title,link,description)
                    except Exception as e:
                        log_error(e)
                        pprint(e)
            client_socket.close()
    except Exception as e:
        log_error(e)
        pprint(e)
    finally:
        if conn:
            conn.close()
        server_socket.close()
        print("Connection et server cloturés.")


if __name__ == "__main__":
    run_server()