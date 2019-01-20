#!/usr/bin/env python
#-*- coding: utf-8 -*-

import sys
reload(sys)
sys.setdefaultencoding('utf 8')
import pywikibot
site = pywikibot.Site()
from wmflabs import db
conn = db.connect('cswiki')

words = [u'zámek', u'hrad']
for word in words:
	firstupperword = word[0].upper() + word[1:]
	cur = conn.cursor()
	with cur:
		sql = 'select page_title, concat("' + word + '_", replace(page_title, "_(' + word + ')", "")) from page where page_title like "%_(' + word + ')" and concat("' + firstupperword + '_", replace(page_title, "_(' + word + ')", "")) not in (select page_title from page) and page_is_redirect=0;'
		cur.execute(sql)
		data = cur.fetchall()
	for row in data:
		page = pywikibot.Page(site, row[1])
		page.text = u"#REDIRECT [[@@TARGET@@]]".replace(u'@@TARGET@@', row[0].replace('_', ' '))
		page.save(u'Robot: Založení přesměrování z dalšího standardního tvaru')
