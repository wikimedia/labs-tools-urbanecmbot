#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot
site = pywikibot.Site()

sql = 'select count(*), lt_title from pagelinks join linktarget on lt_id=pl_target_id where lt_namespace = 0 and pl_from_namespace = 0 and lt_title in (select page_title from page where page_id in (select cl_from from categorylinks where cl_to="Wikipedie:Rozcestníky") and page_namespace=0) group by lt_title order by count(*) desc, lt_title limit 500;'
conn = toolforge.connect('cswiki')
cur = conn.cursor()
with cur:
	cur.execute(sql)
	data = cur.fetchall()

res = ""
for row in data:
	rowres = "# [[" + row[1].decode('utf-8') + "]] ([[Speciální:Co odkazuje na/" + row[1].decode('utf-8') + "|" + str(row[0]) + " odkazů]])"
	res += rowres + '\n'


page = pywikibot.Page(site, "Wikipedie:Údržbové seznamy/Nejvíce odkazované rozcestníky/seznam")
page.text = res
page.save('Robot: Aktualizace seznamu nejodkazovanějších rozcestníků')
