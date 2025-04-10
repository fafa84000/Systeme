import sqlite3
import socket
import os

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
    c = conn.cursor()
    c.execute(
        "INSERT INTO sonde_data (sonde_name, server, data) VALUES (?, ?, ?)",
        (sonde_name, server, data),
    )
    conn.commit()

def run_server():
    conn = init_db()
    host = "localhost"
    port = 5000

    server_socket = socket.socket()
    server_socket.bind((host, port))

    print(f"Serveur démarré sur {host}:{port}, en attente de connexions...")

    try:
        while True:
            num_files = len([f for f in os.listdir("sondes") if os.path.isfile(os.path.join("sondes", f))])
            server_socket.listen(num_files)
            print(f"Nombre de connexions simultanées autorisées : {num_files}")

            client_socket, address = server_socket.accept()
            print(f"Connexion acceptée de {address}")

            data = client_socket.recv(1024).decode('utf-8')
            if data:
                print(f"Données reçues : {data}")
                try:
                    server, sonde_name, sonde_data = data.split('\t', 2)
                    store_data_in_db(conn, sonde_name, server, sonde_data)
                except ValueError:
                    print("Erreur : Format de données incorrect.")
            client_socket.close()
    except KeyboardInterrupt:
        print("\nArrêt du serveur...")
    finally:
        conn.close()
        server_socket.close()

if __name__ == "__main__":
    run_server()
