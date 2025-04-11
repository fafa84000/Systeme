import psutil
import socket
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOST,PORT

def data():
    return psutil.cpu_percent(interval=1)

def sonde_send(host,port):
    client_socket = socket.socket()
    client_socket.connect((host, port))

    message = f"sonde\t{socket.gethostname()}\tcpu\t{data()}"
    client_socket.send(message.encode())

    client_socket.close()


if __name__ == '__main__':
    sonde_send(HOST,PORT)