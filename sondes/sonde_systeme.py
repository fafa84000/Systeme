#!/usr/bin/env python3

import psutil
import os
from datetime import datetime

print("=== SONDE SYSTÈME ===")
print("|| Horodatage :", datetime.now())

print("|| Utilisation CPU (%):", psutil.cpu_percent(interval=1))

mem = psutil.virtual_memory()
print("|| Mémoire utilisée (%):",mem.percent)

print("|| Nombre de processus actifs:", len(psutil.pids()))

print("|| Utilisateurs connectés:", len(psutil.users()))
