# bots
Various simple bots for Czech Wikipedia. 

Scripts daily.sh, weekly.sh and hourly.sh are executed daily/weekly/hourly by cron at WMF Toolsforge. In addition to those three scripts, additional scripts might be executed. I try to include most of those tasks in daily/weekly/hourly script, but there are some situations when other periodicity is required. 

Current crontab is published below together with my comments. 

```
0 5 * * * jlocal rm -rf /home/urbanecm/tmp/* # Clean user's temp
0 5 * * * jlocal rm -rf /data/project/urbanecmbot/tmp/* # Clean user's temp
0 22 * * *  /usr/bin/jsub -N miscTasksDaily -once -quiet bash /data/project/urbanecmbot/11bots/daily.sh  \&\>\> /data/project/urbanecmbot/logs/miscTasksDaily.log # Run daily jobs
0 22 * * 1  /usr/bin/jsub -N miscTasksWeekly -once -quiet bash /data/project/urbanecmbot/11bots/weekly.sh \&\>\> /data/project/urbanecmbot/logs/miscTasksWeekly.log # Run weekly jobs
0 * * * * /usr/bin/jsub -N miscTasksHourly -once -quiet bash /data/project/urbanecmbot/11bots/hourly.sh \&\>\> /data/project/urbanecmbot/logs/miscTasksHourly.log # Run hourly jobs
*/5 * * * * /usr/bin/jsub -N afdNoticesZlobot -once -quiet python /data/project/urbanecmbot/afdHelper/zlobot-afd-notices.py # Run afd notifier - needs to be run each 5 minutes
*/5 * * * * /usr/bin/jsub -N cleanSandbox -once -quiet python /data/project/urbanecmbot/11bots/clean_sandbox.py # Clean sandbox
```
