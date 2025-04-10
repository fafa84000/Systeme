import sqlite3
import socket
import os
import threading

DATABASE_FILE = 'monitoring.db'

def init_db():
    conn = sqlite3.connect(DATABASE_FILE)
    c = conn.cursor()
    c.execute(
        """
        CREATE TABLE IF NOT EXISTS sonde_data (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sonde_name TEXT NOT NULL,
            server TEXT NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            data NUMERIC NOT NULL
        )
        """
    )
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

def count_files_in_directory():
    return len([f for f in os.listdir("sondes") if os.path.isfile(os.path.join("sondes", f)) and f.split('.')[-2].endswith("_sonde")])

def run_server():
    conn = init_db()
    host = "localhost"
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    print(f"Serveur démarré sur {host}:{port}, en attente de connexions...")

    try:
        while True:
            num_files = count_files_in_directory()
            server_socket.listen(num_files)
            print(f"Nombre de connexions simultanées autorisées : {num_files}")

            client_socket, address = server_socket.accept()
            print(f"Connexion acceptée de {address}")

            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Données reçues : {data}")
                if data == "update sondes":
                    continue
                try:
                    server, sonde_name, sonde_data = data.split('\t', 2)
                    store_data_in_db(conn, sonde_name, server, sonde_data)
                except ValueError:
                    print("Erreur : Format de données incorrect.")
            client_socket.close()
    except KeyboardInterrupt:
        conn.close()
        server_socket.close()

def monitor_directory():
    previous_count = count_files_in_directory()
    
    while True:
        current_count = count_files_in_directory()
        if current_count != previous_count:
            host = "localhost"
            port = 5000

            client_socket = socket.socket()
            client_socket.connect((host, port))

            message = "update sondes"
            client_socket.send(message.encode())

            client_socket.close()

            previous_count = current_count

if __name__ == "__main__":
    thread = threading.Thread(target=monitor_directory)
    thread.start()
    run_server()
    
    
