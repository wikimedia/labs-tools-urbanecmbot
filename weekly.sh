#!/bin/bash

export LC_ALL=en_US.UTF-8
python /shared/pywikipedia/core/scripts/archivebot.py Archivace &>> /data/project/urbanecmbot/logs/archivePages.log
python3 /data/project/urbanecmbot/11bots/did_you_know.py -current &>> /data/project/urbanecmbot/logs/did_you_know.log
PYWIKIBOT2_DIR=/data/project/urbanecmbot/autoprotect python /data/project/urbanecmbot/autoprotect/weekly.py
