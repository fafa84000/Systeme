#!/bin/bash

echo "=== SONDE DISQUE ==="

df -h | grep '^/dev/' | while read ligne; do
	echo "|| $ligne"
done
