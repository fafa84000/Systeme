#!/usr/bin/env python3

from requests import get
from xmltodict import parse as parseXML
from socket import socket
from sys import path as pathSys
from os import path as pathOs

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from config import HOST, PORT, ALERTS_URL
from log_manager import log_error

def data():
    try:
        response = get(ALERTS_URL)
        response.raise_for_status()

        xml_content = response.content
        parsed_xml = parseXML(xml_content)
        alerte = parsed_xml['rss']['channel']['item'][-1]
        
        return alerte
    except Exception as e:
        log_error(e)
        return None

def send_data():
    alerte = data()

    if alerte:
        title = alerte['title']
        link = alerte['link']
        description = alerte['description']
        
        try:
            client_socket = socket()
            client_socket.connect((HOST, PORT))

            message = f"alerte\t{title}\t{link}\t{description}"
            client_socket.send(message.encode())

            client_socket.close()
        except Exception as e:
            log_error(e)


if __name__ == "__main__":
    send_data()
