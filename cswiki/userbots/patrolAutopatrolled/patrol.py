#!/usr/bin/env python
#-*- coding: utf-8 -*-

from wmflabs import db
conn = db.connect('cswiki')
import pywikibot
site = pywikibot.Site()


ids = []
with conn.cursor() as cur:
	sql = 'select rc_id from recentchanges where rc_namespace!=8 and rc_patrolled=0 and rc_user in (select distinct ug_user from user_groups where ug_group in ("autopatrolled", "bot", "sysop")) order by rc_timestamp desc'
	cur.execute(sql)
	data = cur.fetchall()
	for row in data:
		ids.append(row[0])

users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolSemitrusted/users.txt', 'r').read().split('\n')
for user in users:
	with conn.cursor() as cur:
		sql = 'select rc_id from recentchanges where rc_namespace!=8 and rc_patrolled=0 and rc_user_text="%s"' % user
		cur.execute(sql)
		data = cur.fetchall()
		for row in data:
			ids.append(row[0])

for id in ids:
	try:
		list(site.patrol(rcid=id))
	except:
		pass
