#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
import pywikibot
import toolforge

conn = toolforge.connect('cswiki', cluster='analytics')
site = pywikibot.Site()

chars = {'—': '-', '…': '...'}
#Generate SQLs
sqls = []
for char in chars:
	sqls.append('select replace(page_title, "' + char + '", "' + chars[char] + '"), page_title from page where page_title like "%' + char + '%" and replace(page_title, "' + char + '", "' + chars[char] + '") not in (select page_title from page) and page_namespace=0 and page_is_redirect=0;')

#And fetch data...
data = []
for sql in sqls:
	cur = conn.cursor()
	with cur:
		cur.execute(sql)
		d = cur.fetchall()
	for row in d:
		data.append(row)

# Create the redirects
for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'))
	page.text = '#REDIRECT [[' + row[1].decode('utf-8') + ']]'
	page.save('Robot: Přidání přesměrování')
