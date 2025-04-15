import sqlite3
import socket
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOST,PORT,PROBES_DIRECTORY,FIND,DATABASE_FILE,SQL

def read_sql_file():
    with open(SQL, 'r', encoding='utf-8') as file:
        return file.read()

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    stmts = read_sql_file().split(';')
    for stmt in stmts:
        c.execute(stmt)
    conn.commit()
    return conn

def store_data_in_db(conn, sonde_name, server, data):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO sonde_data (sonde_name, server, data)
        VALUES (?, ?, ?)
        """,
        (sonde_name, server, data)
    )
    conn.commit()

def store_alerte_in_db(conn, title, link, description):
    c = conn.cursor()
    c.execute(
        """
        INSERT INTO alertes (title, link, description)
        SELECT ?, ?, ?
        WHERE NOT EXISTS (
            SELECT 1 FROM alertes WHERE link = ?
        );
        """,
        (title, link, description, link)
    )
    conn.commit()


def count_files_in_directory():
    return len([f for f in os.listdir(PROBES_DIRECTORY) if f.split('.')[-2].endswith(FIND)])

def run_server(conn):
    server_socket = socket.socket()
    server_socket.bind((HOST, PORT))

    try:
        while True:
            num_files = count_files_in_directory()
            server_socket.listen(num_files)

            client_socket, address = server_socket.accept()

            data = client_socket.recv(1024).decode('utf-8')
            if data:
                if data[0] == "u":
                    continue
                elif data[0] == "s":
                    try:
                        type, server, sonde_name, sonde_data = data.split('\t')
                        store_data_in_db(conn, sonde_name, server, sonde_data)
                    except ValueError:
                        print("Erreur : Format de données incorrect.")
                elif data[0] == "a":
                    print(data.split('\t'))
                    try:
                        type,title,link,description = data.split('\t')
                        store_alerte_in_db(conn,title,link,description)
                    except ValueError:
                        print("Erreur : Format de données incorrect.")
            client_socket.close()
    except KeyboardInterrupt:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    conn = init_db()

    run_server(conn)