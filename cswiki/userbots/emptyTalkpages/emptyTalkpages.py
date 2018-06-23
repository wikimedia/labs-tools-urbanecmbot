#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

conn = toolforge.connect('cswiki')
site = pywikibot.Site()

with conn.cursor() as cur:
	cur.execute('select page_title, page_namespace from page where page_len=0 and page_namespace in (1) and page_is_redirect=0;')
	data = cur.fetchall()

exceptions = pywikibot.Page(site, "User:UrbanecmBot/Záměrně prázdné diskusní stránky").text.split('\n')

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=row[1])
	if page.title() in exceptions: continue
	page.delete("prázdná diskusní stránka", mark=True)
