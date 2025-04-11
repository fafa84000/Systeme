#!/bin/bash

echo -e "sonde\t`hostname`\tusers\t`who | wc -l`" | nc -N $(python3 /path/config.py 1);