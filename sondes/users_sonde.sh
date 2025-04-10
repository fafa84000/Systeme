#!/bin/bash

echo "`hostname`    users   `who | wc -l`" | nc -N FA 5000;