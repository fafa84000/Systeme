from socket import socket, gethostname
from sys import path as pathSys
from os import path as pathOs

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import HOST,PORT
from log_manager import log_error

def sonde_send(name,data):
    try:
        with socket() as client_socket:
            client_socket.connect((HOST, PORT))
            message = f"sonde\t{gethostname()}\t{name}\t{data}"
            client_socket.send(message.encode())
    except Exception as e:
        log_error(e)