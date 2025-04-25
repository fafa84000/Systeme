from psutil import cpu_percent

def data():
    return cpu_percent(interval=1)