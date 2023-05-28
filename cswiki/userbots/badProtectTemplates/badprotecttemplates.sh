#!/bin/bash

source ~/venv/bin/activate

#python3 ~/pwb/scripts/blockpageschecker.py -always
#python3 ~/pwb/scripts/blockpageschecker.py -catr:"Údržba:Stránky s chybným použitím šablony o zamčení" -always
python3 ~/pwb/scripts/blockpageschecker.py -catr:"Údržba:Stránky s chybným použitím šablony o zamčení" -ns:0 -always
