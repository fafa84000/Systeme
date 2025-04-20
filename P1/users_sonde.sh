#!/bin/bash

echo -e "sonde\t`hostname`\tusers\t`who | wc -l`" | nc -N $(python3 /home/uapv2306164/Systeme/config.py print);