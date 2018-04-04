#!/bin/bash

cd /data/project/urbanecmbot/11bots
crontab -l > cron.txt
git commit -am "Update cron.txt"
git push
