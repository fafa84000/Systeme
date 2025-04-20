from psutil import cpu_percent
from sendSonde import sonde_send

def data():
    return cpu_percent(interval=1)

if __name__ == '__main__':
    sonde_send('cpu',data())