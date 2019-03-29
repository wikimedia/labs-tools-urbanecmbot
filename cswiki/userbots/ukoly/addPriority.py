#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import toolforge
import pywikibot
site = pywikibot.Site()
conn = toolforge.connect('cswiki', cluster='analytics')

def getPriority(links):
	if links >= 500:
		return 1
	elif links >= 250:
		return 2
	elif links >= 100:
		return 3
	elif links >= 50:
		return 4
	elif links >= 20:
		return 5
	elif links >= 10:
		return 6
	elif links >= 5:
		return 7
	elif links >= 2:
		return 8
	else:
		return 9

cur = conn.cursor()
with cur:
	sql = 'select page_title, page_namespace from categorylinks join page on cl_from=page_id where cl_to="Údržba:Úkoly_bez_vyznačené_priority" and page_namespace%2=1'
	cur.execute(sql)
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=int(row[1]))
	if not page.exists():
		continue
	cur = conn.cursor()
	with cur:
		sql = 'select count(*) from pagelinks where pl_title="' + row[0].decode('utf-8') + '"'
		cur.execute(sql)
		links = cur.fetchall()[0][0]
	priority = getPriority(links)
	text = page.text
	page.text = re.sub(r'{{Úkoly}}', '{{Úkoly|' + str(priority) + '}}', text, flags=re.IGNORECASE)
	page.save('Robot: Doplnění priority k šabloně úkoly')
