#!/bin/bash

wget -qO- "$1" | cut -f2 | sed 1d > /tmp/$$.txt
python3 ~/pwb/scripts/coordinate_import.py -file:"/tmp/$$.txt" -maxlag:20 $2
rm /tmp/$$.txt
