#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
from wmflabs import db

# Connect to database
conn = db.connect('cswiki')

# Get all relevant page titles from the database
cur = conn.cursor()
with cur:
	sql = 'select page_title from page where page_namespace=828 and page_title like "Wikidata/%" and page_title not like "%/testcases%" and page_title not like "%/Dokumentace%" and page_title not like "%/sandbox%" and page_title!="Wikidata/";'
	cur.execute(sql)
	data = cur.fetchall()

# Create site objects
siteour = pywikibot.Site()
siteforegin = pywikibot.Site('cs', 'wikiversity')

# Create summary constant
summary = u'Robot: Aktualizace Wikidata modulů'

# Export Modul:Wikidata
pageour = pywikibot.Page(siteour, u'Modul:Wikidata')
pageforegin = pywikibot.Page(siteforegin, u'Modul:Wikidata')
pageforegin.text = pageour.text
pageforegin.save(summary)

# Export all other Modul:Wikidata subpages
for row in data:
	pagetitle = 'Modul:' + row[0]
	pageour = pywikibot.Page(siteour, pagetitle)
	pageforegin = pywikibot.Page(siteforegin, pagetitle)
	newtext = '-- Tato stránka je pravidelně aktualizována robotem. Jakákoliv modifikace bude při příští aktualizaci přepsána a je třeba ji provádět na Wikipedii. \n\n' + pageour.text
	pageforegin.text = newtext
	pageforegin.save(summary)
