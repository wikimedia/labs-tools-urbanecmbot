#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import re
import toolforge

RE_BRACKETS = re.compile(r'\(.*\)$')

wikidataSite = pywikibot.Site('wikidata', 'wikidata')
cswikiSite = pywikibot.Site('cs', 'wikipedia')
conn = toolforge.connect('cswiki')

titles = []
with conn.cursor() as cur:
	cur.execute("select page_title from categorylinks join page on cl_from=page_id where page_namespace=0 and cl_to='Údržba:Články_bez_štítku_na_Wikidatech'")
	data = cur.fetchall()
	for row in data:
		titles.append(row[0].decode('utf-8').replace('_', ' '))

for title in titles:
	cswikiPage = pywikibot.Page(cswikiSite, title)
	try:
		item = pywikibot.ItemPage.fromPage(cswikiPage)
	except pywikibot.exceptions.NoPageError:
		continue
	if item.get().get('labels', {}).get('cs') is not None:
		cswikiPage.touch()  # to remove the "no Wikidata label" category
		continue

	label = RE_BRACKETS.sub('', title).strip()
	item.editLabels(labels={'cs': label}, summary='Add Czech label: %s' % label)
	cswikiPage.touch()  # to remove the "no Wikidata label" category
