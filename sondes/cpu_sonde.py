import psutil
import socket

def data():
    return psutil.cpu_percent(interval=1)

def sonde_send():
    host = "localhost"
    port = 5000

    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = f"{host}\tcpu\t{data()}"
    client_socket.send(message.encode())

    client_socket.close()


if __name__ == '__main__':
    sonde_send()