#!/usr/bin/env python
#-*- coding: utf-8 -*-

import re
import toolforge
import pywikibot

conn = toolforge.connect('cswiki', cluster='analytics')
site = pywikibot.Site()

with conn.cursor() as cur:
	cur.execute('select page_title, page_namespace from categorylinks join page on cl_from=page_id where cl_to="Údržba:Stránky_ke_smazání" and page_namespace%2=1 and page_title like "%/Úkoly";')
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=row[1])
	print(page)
	do_delete = len(re.findall(r'{{Smazat\|úkoly vyřešeny}}', page.text)) == 1
	if do_delete:
		page.delete('Robot: Úkoly vyřešeny', prompt=False)
