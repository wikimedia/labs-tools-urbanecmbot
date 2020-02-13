#!/usr/bin/env python
#-*- coding: utf-8 -*-

from wmflabs import db
import pywikibot
site = pywikibot.Site()

sql = 'select count(*), pl_title from pagelinks where pl_namespace=0 and pl_from_namespace = 0 and pl_title in (select page_title from page where page_id in (select cl_from from categorylinks where cl_to="Wikipedie:Rozcestníky") and page_namespace=0) group by pl_title order by count(*) desc, pl_title limit 500;'
conn = db.connect('cswiki')
cur = conn.cursor()
with cur:
	cur.execute(sql)
	data = cur.fetchall()

res = ""
for row in data:
	rowres = "# [[" + row[1].decode('utf-8') + "]] ([[Speciální:Co odkazuje na/" + row[1].decode('utf-8') + "|" + str(row[0]) + " odkazů]])"
	res += rowres + '\n'


page = pywikibot.Page(site, u"Wikipedie:Údržbové seznamy/Nejvíce odkazované rozcestníky/seznam")
page.text = res
page.save(u'Robot: Aktualizace seznamu nejodkazovanějších rozcestníků')
