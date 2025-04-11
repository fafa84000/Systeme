import socket
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import *

def count_files_in_directory():
    return len([f for f in os.listdir(PROBES_DIRECTORY) if f.split('.')[-2].endswith(FIND)])

def update():
    previous_count = count_files_in_directory()
    
    while True:
        current_count = count_files_in_directory()
        if current_count != previous_count:

            client_socket = socket.socket()
            client_socket.connect((HOST, PORT))

            message = "update sondes number"
            client_socket.send(message.encode())

            client_socket.close()

            previous_count = current_count

if __name__ == '__main__':
    update()