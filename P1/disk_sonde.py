from psutil import disk_usage
from sendSonde import sonde_send

def data():
    return disk_usage('/').percent

if __name__ == '__main__':
    sonde_send('disk',data())