#!/usr/bin/env python
#-*- coding: utf-8 -*-

from datetime import datetime
from datetime import timedelta
import toolforge
conn = toolforge.connect('cswiki')
import pywikibot
site = pywikibot.Site()

with conn.cursor() as cur:
	cur.execute('select rev_timestamp from revision where rev_page=(select page_id from page where page_namespace=4 and page_title="Pískoviště") order by rev_id desc')
	data = cur.fetchall()
if data[0][0] < (datetime.now() + timedelta(minutes=15)).strftime('%Y%m%d%H%M%S'):
	page = pywikibot.Page(site, u"Wikipedie:Pískoviště")
	page.text = open('/data/project/urbanecmbot/11bots/cswiki/userbots/cleanSandbox/vzor.txt').read()
	page.save('Robot: Úhrab pískoviště')

with conn.cursor() as cur:
	cur.execute('select rev_timestamp from revision where rev_page=(select page_id from page where page_namespace=10 and page_title="Test") order by rev_id desc')
	data = cur.fetchall()
if data[0][0] < (datetime.now() + timedelta(minutes=180)).strftime('%Y%m%d%H%M%S'):
	page = pywikibot.Page(site, u"Šablona:Test")
	page.text = open('/data/project/urbanecmbot/11bots/cswiki/userbots/cleanSandbox/vzor_sablona.txt').read()
	page.save('Robot: Úhrab pískoviště')

with conn.cursor() as cur:
	cur.execute('select rc_id from revision join recentchanges on rc_this_oldid=rev_id where rev_page in (3008, 5264) and rc_patrolled=0;')
	data = cur.fetchall()

for row in data:
	try:
		list(site.patrol(rcid=row[0]))
	except:
		pass
