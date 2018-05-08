#!/bin/bash

wget -qO- "$1" | cut -f2 | sed 1d > /tmp/$$.txt
python ~/pwb/scripts/coordinate_import.py -file:"/tmp/$$.txt" $2
rm /tmp/$$.txt
