#!/bin/bash

export LC_ALL=en_US.UTF-8
python /data/project/urbanecmbot/mark-students/cache.py # Regenerate stylesheet that greens students
PYWIKIBOT2_DIR=/data/project/urbanecmbot/11bots/sysopbots python /data/project/urbanecmbot/11bots/sysopbots/purgeKonecMazani.py
