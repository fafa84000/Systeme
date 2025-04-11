import requests
import xml.etree.ElementTree as ET
import xmltodict
import pprint

url = "https://www.cert.ssi.gouv.fr/alerte/feed/"

def data():
    try:
        response = requests.get(url)
        response.raise_for_status()  # Vérifie les erreurs HTTP

        xml_content = response.content
        parsed_xml = xmltodict.parse(xml_content)
        alertes = parsed_xml['rss']['channel']['item']

        

    except requests.exceptions.RequestException as e:
        print(f"Erreur lors de la récupération du flux: {e}")