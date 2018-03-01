#!/bin/bash

export LC_ALL=en_US.UTF-8
python /data/project/urbanecmbot/mark-students/cache.py # Regenerate stylesheet that greens students
python /data/project/urbanecmbot/11bots/purgeKonecMazani.py
