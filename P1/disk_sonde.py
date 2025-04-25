from psutil import disk_usage

def data():
    return disk_usage('/').percent