#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime
import toolforge
import pywikibot
conn = toolforge.connect('cswiki')
site = pywikibot.Site()

page = pywikibot.Page(site, u"Wikipedie:Pískoviště")
if (datetime.now() - page.editTime()).seconds / 60 / 60 > 2:
	page.text = open('/data/project/urbanecmbot/11bots/cswiki/userbots/cleanSandbox/vzor.txt').read()
	page.save('Robot: Úhrab pískoviště')

page = pywikibot.Page(site, u"Šablona:Test")
if (datetime.now() - page.editTime()).seconds / 60 / 60 > 8:
	page.text = open('/data/project/urbanecmbot/11bots/cswiki/userbots/cleanSandbox/vzor_sablona.txt').read()
	page.save('Robot: Úhrab pískoviště')

with conn.cursor() as cur:
	cur.execute('select rc_id from revision join recentchanges on rc_this_oldid=rev_id where rev_page in (3008, 5264) and rc_patrolled=0;')
	data = cur.fetchall()

for row in data:
	try:
		list(site.patrol(rcid=row[0]))
	except Exception:
		pass
