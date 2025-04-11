#!/bin/bash

for file in /path/to/directory/*; do
  if [[ -f "$file" ]]; then
    ./"$file"
    sleep 60
  fi
done
