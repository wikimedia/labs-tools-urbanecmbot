#!/bin/bash

cd /data/project/urbanecmbot/11bots/cswiki/userbots/patrolAutopatrolled
echo 'select rc_id from recentchanges where rc_namespace!=8 and rc_patrolled=0 and rc_user in (select distinct ug_user from user_groups where ug_group in ("autopatrolled", "bot", "sysop")) order by rc_timestamp desc' | sql cswiki | sed 1d > topatrol.txt
python patrol.py
cd $OLDPWD
