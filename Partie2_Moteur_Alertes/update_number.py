import socket
import os
import sys
from config import *

def count_files_in_directory(directory,find):
    return len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f)) and f.split('.')[-2].endswith(find)])

def update(host,port,directory,find):
    previous_count = count_files_in_directory(directory,find)
    
    while True:
        current_count = count_files_in_directory(directory,find)
        if current_count != previous_count:
            client_socket = socket.socket()
            client_socket.connect((host, port))

            message = "update sondes number"
            client_socket.send(message.encode())

            client_socket.close()

            previous_count = current_count

if __name__ == '__main__':
    update(HOST,PORT,PROBES_DIRECTORY,FIND)