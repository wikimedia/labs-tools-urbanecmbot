#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

conn = toolforge.connect('cswiki')
site = pywikibot.Site()

with conn.cursor() as cur:
	cur.execute('select page_title from page where page_len=0 and page_namespace=4 and page_title like "Nástěnka/%";')
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=4)
	page.delete("prázdná stránka kurzu, kurz byl smazán na nástěnce", mark=True)
