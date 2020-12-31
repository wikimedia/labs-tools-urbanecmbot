#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot
import mwparserfromhell
import re

site = pywikibot.Site()
commonsSite = pywikibot.Site('commons', 'commons')
conn = toolforge.connect('cswiki')
commonsConn = toolforge.connect('commonswiki')

RE_COMMONSCAT = re.compile(r'(\* )?\{\{[cC]ommonscat(\|[^}]*)?\}\}')

with conn.cursor() as cur:
	cur.execute('select page_title, page_namespace from categorylinks join page on page_id=cl_from where cl_to="Údržba:Commonscat_není_na_Wikidatech"')
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'), ns=row[1])
	print(page.title())
	code = mwparserfromhell.parse(page.text)
	cat_exists = None
	for tmpl in code.filter_templates():
		if tmpl.name.lower() == 'commonscat':
			print(tmpl)
			print(tmpl.params)
			cat_name = row[0].decode('utf-8')
			for param in tmpl.params:
				if param.name == '1':
					if param.value != '':
						cat_name = param.value.strip()
					break
			commonsCat = pywikibot.Page(commonsSite, cat_name, ns=14)
			print(commonsCat.title())
			cat_exists = commonsCat.exists()
			break
	if cat_exists is None:
		continue

	if cat_exists is False:
		with commonsConn.cursor() as cur:
			cur.execute('select count(*) from categorylinks where cl_to="%s"' % cat_name)
			numOfFiles = cur.fetchall()[0][0]
		if numOfFiles == 0:
			page.text = RE_COMMONSCAT.sub('', page.text)
			page.save('Robot: Smazání šablony Commonscat odkazující na neexistující Commons kategorii', minor=False, botflag=False)
	else:
		print('Not in Wikidata for %s' % page.title())
