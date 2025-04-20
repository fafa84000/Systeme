from sys import path as pathSys
from os import path as pathOs
from smtplib import SMTP_SSL
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

pathSys.append(pathOs.dirname(pathOs.dirname(pathOs.abspath(__file__))))
from log_manager import log_error

def message(sujet,texte):
    message = MIMEMultipart()
    message['From'] = 'farouk.assim@alumni.univ-avignon.fr'
    message['To'] = 'farouk.assim@alumni.univ-avignon.fr'
    message['Subject'] = sujet
    texteMessage = texte
    message.attach(MIMEText(texteMessage))
    return message

def send_mail(sujet,texte):
    mail_server = None
    try:
        mail_server = SMTP_SSL('partage.univ-avignon.fr', 465)
        mail_server.ehlo()
        mail_server.login('farouk.assim@alumni.univ-avignon.fr','zuphuh-kupni9-Ragpox')
        mail_server.sendmail('farouk.assim@alumni.univ-avignon.fr','farouk.assim@alumni.univ-avignon.fr',message(sujet,texte).as_string())
    except Exception as e:
        log_error(e)
    finally:
        if mail_server:
            try:
                mail_server.quit()
            except Exception:
                pass