#!/bin/sh
# script that loops and runs the killstream python file

while [ : ]
do
    clear
    cd /YOURPATH/Killstream && python3 killstream.py
    sleep 2
    echo "Sleeping..."
    sleep 20
done