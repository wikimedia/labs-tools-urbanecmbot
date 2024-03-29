#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import pywikibot
import re
import toolforge
site = pywikibot.Site()
conn = toolforge.connect('cswiki', cluster='analytics')

cur = conn.cursor()
with cur:
	sql = 'select page_title, page_namespace from categorylinks join page on cl_from=page_id where cl_to="Údržba:Šablona_Úkoly_bez_podstránky" and page_namespace%2=1'
	cur.execute(sql)
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=row[1])
	if not page.exists():
		continue
	text = page.text
	text = re.sub(r'{{Úkoly\|?[\d]*}}', '', text, flags=re.IGNORECASE)
	print(page)
	if text.strip() == '':
		page.delete(reason=u"Robot: Úkoly vyřešeny", prompt=False)
	else:
		page.text = text
		page.save('Robot: Odebrání šablony úkoly', force=True)
