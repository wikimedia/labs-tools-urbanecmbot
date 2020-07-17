#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot

site = pywikibot.Site()
conn = toolforge.connect('cswiki', cluster='analytics')

with conn.cursor() as cur:
	cur.execute('select user_name from user_groups join user on ug_user=user_id where ug_group="autopatrolled"')
	data = cur.fetchall()

autopatrolled = []
for row in data:
	autopatrolled.append(row[0].decode('utf-8'))

page = pywikibot.Page(site, 'Wikipedista:UrbanecmBot/EditPatrol')
usersOrig = page.text.split('\n')
usersOrig.pop(0)
usersOrig.pop()
usersOrig.sort()

users = []
for user in usersOrig:
	if user not in autopatrolled:
		users.append(user)

page.text = '<pre>\n' + '\n'.join(users) + '\n</pre>'
page.save('Robot: Seřazení seznamu, odebrání prověřených uživatelů')
