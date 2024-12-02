#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

site = pywikibot.Site()
conn = toolforge.connect('cswiki', cluster='analytics')

with conn.cursor() as cur:
	cur.execute("select t.page_namespace, t.page_title, s.page_title from page as t left join page as s on ((t.page_namespace = s.page_namespace) and (replace(t.page_title, '/Úkoly', '') = s.page_title)) where t.page_namespace % 2 = 1 and t.page_title like '%/Úkoly' and s.page_title is null")
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])
	if not page.exists():
		print('INFO: Skipping %s' % page.title())
		continue

	page.delete(reason='Robot: Smazání šablony úkoly bez příslušné nadstránky', prompt=False)
