#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()
import toolforge
conn = toolforge.connect('cswiki', cluster='analytics')

words = ['zámek', 'hrad']
for word in words:
	firstupperword = word[0].upper() + word[1:]
	cur = conn.cursor()
	with cur:
		sql = 'select page_title, concat("' + word + '_", replace(page_title, "_(' + word + ')", "")) from page where page_title like "%_(' + word + ')" and concat("' + firstupperword + '_", replace(page_title, "_(' + word + ')", "")) not in (select page_title from page) and page_is_redirect=0;'
		cur.execute(sql)
		data = cur.fetchall()
	for row in data:
		page = pywikibot.Page(site, row[1].decode('utf-8'))
		page.text = "#REDIRECT [[@@TARGET@@]]".replace('@@TARGET@@', row[0].decode('utf-8').replace('_', ' '))
		page.save('Robot: Založení přesměrování z dalšího standardního tvaru')
