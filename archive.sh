#!/bin/bash

export LC_ALL=en_US.UTF-8
python /shared/pywikipedia/core/scripts/archivebot.py Archivace &>> /data/project/urbanecmbot/logs/archivePages.log
