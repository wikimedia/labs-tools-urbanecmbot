#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pywikibot
import re
site = pywikibot.Site()
from wmflabs import db
conn = db.connect('cswiki')

cur = conn.cursor()
with cur:
	sql = 'select page_title from categorylinks join page on cl_from=page_id where cl_to="Údržba:Šablona_Úkoly_bez_podstránky" and page_namespace%2=1'
	cur.execute(sql)
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=1)
	page.purge()

time.sleep(10) # Wait for replicating changed category to Toolsforge

cur = conn.cursor()
with cur:
	sql = 'select page_title from categorylinks join page on cl_from=page_id where cl_to="Údržba:Šablona_Úkoly_bez_podstránky" and page_namespace%2=1'
	cur.execute(sql)
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=1)
	text = page.text.encode('utf-8')
	text = re.sub(r'{{Úkoly\|?[\d]*}}', '', text, flags=re.IGNORECASE)
	if text.strip() == '':
		page.delete(reason=u"Robot: Úkoly vyřešeny", mark=True)
	else:
		page.text = text.decode('utf-8')
		page.save('Robot: Odebrání šablony úkoly')
