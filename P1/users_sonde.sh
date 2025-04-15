#!/bin/bash

echo -e "sonde\t`hostname`\tusers\t`who | wc -l`" | nc -N $(python3 ~/Systeme/config.py 1);