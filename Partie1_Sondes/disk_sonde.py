import psutil
import socket
import sys
from config import HOST,PORT

def data():
    return psutil.disk_usage('/').percent

def sonde_send(host,port):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = f"sonde\t{socket.gethostname()}\tdisk\t{data()}"
    client_socket.send(message.encode())

    client_socket.close()


if __name__ == '__main__':
    sonde_send(HOST,PORT)