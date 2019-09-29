#!/usr/bin/env python
#-*- coding: utf-8 -*-

import logging
import toolforge
conn = toolforge.connect('cswiki')
import pywikibot
site = pywikibot.Site()

logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolAutopatrol.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

ids = []
with conn.cursor() as cur:
	sql = 'select rc_id from recentchanges join actor on rc_actor=actor_id where rc_namespace!=8 and rc_patrolled=0 and actor_user!=0 and actor_name in (select distinct ug_user from user_groups where ug_group in ("autopatrolled", "bot", "sysop")) order by rc_timestamp desc'
	cur.execute(sql)
	data = cur.fetchall()
	for row in data:
		ids.append(row[0])

users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt', 'r').read().split('\n')
for user in users:
	with conn.cursor() as cur:
		sql = 'select rc_id from recentchanges join actor on rc_actor=actor_id where rc_namespace!=8 and rc_patrolled=0 and actor_user!=0 and actor_name="%s" and rc_new=0' % user
		cur.execute(sql)
		data = cur.fetchall()
		for row in data:
			ids.append(row[0])

users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/trustedpatrol.txt', 'r').read().split('\n')
for user in users:
	with conn.cursor() as cur:
		sql = 'select rc_id from recentchanges join actor on rc_actor=actor_id where rc_namespace!=8 and rc_patrolled=0 and actor_user!=0 and actor_name="%s" and (rc_new=0 or rc_namespace!=0)' % user
		cur.execute(sql)
		data = cur.fetchall()
		for row in data:
			ids.append(row[0])

users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/pagepatrol.txt', 'r').read().split('\n')
for user in users:
	with conn.cursor() as cur:
		sql = 'select rc_id from recentchanges join actor on rc_actor=actor_id where rc_namespace!=8 and rc_patrolled=0 and actor_user!=0 and actor_name="%s"' % user
		cur.execute(sql)
		data = cur.fetchall()
		for row in data:
			ids.append(row[0])

with conn.cursor() as cur:
	cur.execute('select rc_id from recentchanges join comment on comment_id=rc_comment_id where comment_text like "%([[:c:GR|GR]])" and rc_patrolled=0;')
	data = cur.fetchall()
	for row in data:
		ids.append(row[0])

with conn.cursor() as cur:
	cur.execute('select rc_id from recentchanges join comment on comment_id=rc_comment_id where comment_text like "%GlobalReplace v0.6.5%" and rc_patrolled=0;')
	data = cur.fetchall()
	for row in data:
		ids.append(row[0])

for id in ids:
	try:
		list(site.patrol(rcid=int(id)))
		logging.info("Making revision %s as patrolled", id)
	except:
		logging.exception('Unknown exception occured')
