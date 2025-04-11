import sqlite3
import socket
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOST,PORT,PROBES_DIRECTORY,FIND,DATABASE_FILE,SQL

def read_sql_file(file):
    with open(file, 'r', encoding='utf-8') as file:
        return file.read()

def init_db(file,sql):
    conn = sqlite3.connect(file)
    c = conn.cursor()
    c.execute(read_sql_file(sql))
    conn.commit()
    return conn

def store_data_in_db(conn, sonde_name, server, data):
    print("Insertion base de donnée.")
    c = conn.cursor()
    c.execute(
        "INSERT INTO sonde_data (sonde_name, server, data) VALUES (?, ?, ?)",
        (sonde_name, server, data),
    )
    conn.commit()

def store_alerte_in_db(conn):
    print("Insertion base de donnée.")
    c = conn.cursor()
    c.execute(
        """"""
    )
    conn.commit()

def count_files_in_directory(directory,find):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.split('.')[-2].endswith(find)])

def run_server(conn,host,port,directory,find):
    server_socket = socket.socket()
    server_socket.bind((host, port))

    print(f"Serveur démarré sur {host}:{port}, en attente de connexions...")

    try:
        while True:
            num_files = count_files_in_directory(directory,find)
            server_socket.listen(num_files)
            print(f"Nombre de connexions simultanées autorisées : {num_files}")

            client_socket, address = server_socket.accept()
            print(f"Connexion acceptée de {address}")

            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Données reçues : {data}")
                if data[0] == "u":
                    continue
                elif data[0] == "s":
                    try:
                        type, server, sonde_name, sonde_data = data.split('\t')
                        store_data_in_db(conn, sonde_name, server, sonde_data)
                    except ValueError:
                        print("Erreur : Format de données incorrect.")
                elif data[0] == "a":
                    try:
                        type = data.split('\t')
                        store_alerte_in_db(conn)
                    except ValueError:
                        print("Erreur : Format de données incorrect.")
            client_socket.close()
    except KeyboardInterrupt:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    conn = init_db(DATABASE_FILE,SQL)

    run_server(conn,HOST,PORT,PROBES_DIRECTORY,FIND)