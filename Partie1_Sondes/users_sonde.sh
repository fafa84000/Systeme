#!/bin/bash

echo -e "sonde\t`hostname`\tusers\t`who | wc -l`" | nc -N $(python3 ../config.py 1);