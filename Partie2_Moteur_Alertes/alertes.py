import requests
import xmltodict
import pprint
import socket
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HOST,PORT

url = "https://www.cert.ssi.gouv.fr/alerte/feed/"

def data():
    try:
        response = requests.get(url)
        response.raise_for_status()

        xml_content = response.content
        parsed_xml = xmltodict.parse(xml_content)
        alerte = parsed_xml['rss']['channel']['item'][-1]
        
        return alerte

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du flux: {e}")

def send_data():
    alerte = data()

    if alerte:
        title = alerte['title']
        link = alerte['link']
        description = alerte['description']
        
        client_socket = socket.socket()
        client_socket.connect((HOST, PORT))

        message = f"alerte\t{title}\t{link}\t{description}"
        client_socket.send(message.encode())

        client_socket.close()


if __name__ == "__main__":
    send_data()