from psutil import virtual_memory
from sendSonde import sonde_send

def data():
    return virtual_memory().percent

if __name__ == '__main__':
    sonde_send('ram',data())
