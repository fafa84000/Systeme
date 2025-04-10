#!/usr/bin/env python3

import psutil
import subprocess
from datetime import datetime

print("=== SONDE MIXTE ===")
print("|| Horodatage :", datetime.now())

mem = psutil.virtual_memory()
print("|| RAM utilisée (MB):", mem.used // (1024 * 1024), "MB")

uptime = subprocess.getoutput("uptime -p")
print("|| Uptime:", uptime)
