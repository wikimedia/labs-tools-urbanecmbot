#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import pywikibot
site = pywikibot.Site('cs', 'wikipedia')
page = pywikibot.Page(site, u"Wikipedista:UrbanecmBot/EditPatrol")

users = page.text.split('\n')

f = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt', 'w')
for user in users:
	with conn.cursor() as cur:
		sql = "select ug_user from user_groups where ug_user=(select user_id from user where user_name=%s)"
		cur.execute(sql, user)
		data = cur.fetchall()
		if len(data) == 0:
			f.write(user + '\n')
