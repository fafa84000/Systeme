from psutil import virtual_memory

def data():
    return virtual_memory().percent
