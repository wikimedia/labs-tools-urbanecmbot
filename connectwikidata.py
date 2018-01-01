#!/usr/bin/env python
#-*- coding: utf-8 -*-

import mwparserfromhell
import pywikibot
site = pywikibot.Site()
repo = site.data_repository()
import requests

url = 'https://petscan.wmflabs.org/?language=cs&project=wikipedia&categories=%C3%9Adr%C5%BEba%3ANepropojen%C3%A9%20%C4%8Dl%C3%A1nky%20vznikl%C3%A9%20p%C5%99ekladem&ns%5B0%5D=1&show_redirects=no&wikidata_item=without&interface_language=en&active_tab=tab_wikidata&doit=&format=tsv'
r = requests.get(url)
first = True
rows = r.content.split('\n')
rows.pop()
for row in rows:
	if first:
		first = False
		continue
	line = row.split('\t')
	page = pywikibot.Page(site, line[1])
	code = mwparserfromhell.parse(page.text)
	for template in code.filter_templates():
		if template.name == u'Překlad':
			lang = str(template.params[0].value)
			article = str(template.params[1].value)
			forsite = pywikibot.Site(lang, "wikipedia")
			forpage = pywikibot.Page(forsite, article)
			item = forpage.data_item()
			item.setSitelink(page)
			break
	break
