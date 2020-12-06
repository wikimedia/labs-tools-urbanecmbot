#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import toolforge
import pywikibot
conn = toolforge.connect('metawiki')
site = pywikibot.Site('meta', 'meta')

logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolAutopatrolMeta.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

ids = []
with conn.cursor() as cur:
	sql = 'select rc_id from recentchanges join actor on rc_actor=actor_id where rc_namespace!=8 and rc_patrolled=0 and actor_user!=0 and actor_user in (select distinct ug_user from user_groups where ug_group in ("autopatrolled", "bot", "sysop")) order by rc_timestamp desc'
	cur.execute(sql)
	data = cur.fetchall()
	for row in data:
		ids.append(row[0])

for id in ids:
	list(site.patrol(rcid=int(id)))
	logging.info("Making revision %s as patrolled", id)
