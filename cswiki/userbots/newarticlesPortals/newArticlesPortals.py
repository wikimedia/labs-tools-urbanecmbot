#!/usr/bin/env python
# coding=utf-8

# Imports
import requests
import csv
import pywikibot
import datetime
import toolforge

# Config
DEPTH = 5
PORTALS = {
	'Portál:Ptáci/Nové články': 'Ptáci',
	'Portál:Obojživelníci/Nové články': 'Obojživelníci',
}
EXCEPTIONS = {
	'SOME': ['SOME']
}
BASEURL = 'https://petscan.wmflabs.org/'
BASESQL = 'select left(rev_timestamp, 8) from revision where rev_page in (select page_id from page where page_title=%s and page_namespace=0) and rev_parent_id=0;'

BEFORE_DAYS = 30

AFTER_DATE = (datetime.date.today() - datetime.timedelta(days=BEFORE_DAYS)).strftime('%Y%m%d')

# Code
conn = toolforge.connect('cswiki')
site = pywikibot.Site()
for portal in PORTALS:
	pages = {}
	category = PORTALS[portal]
	payload = {
		'language': 'cs',
		'project': 'wikipedia',
		'depth': DEPTH,
		'categories': category,
		'ns[0]': 1,
		'after': AFTER_DATE,
		'only_new': 'on',
		'show_redirects': 'no',
		'interface_language': 'en',
		'format': 'json',
		'doit': 'doit'
	}
	r = requests.get(BASEURL, params=payload)
	data = r.json()
	for page in data['*'][0]['a']['*']:
		with conn.cursor() as cur:
			cur.execute(BASESQL, (page['title'], ))
			dayofcreation = cur.fetchall()[0][0].decode('utf-8')
		pages[dayofcreation] = page['title']
	dateofcreations = list(pages.keys())
	dateofcreations.sort()
	wikicode = "<!-- Prosím, nepřepisujte tuto stránku, příští noc budou změny přepsány botem -->\n\n"
	for dateofcreationraw in dateofcreations:
		page = pages[dateofcreationraw]
		dateofcreation = datetime.datetime.strptime(dateofcreationraw, '%Y%m%d')
		dateofcreationhuman = "{0}. {1}. {2}".format(dateofcreation.day, dateofcreation.month, dateofcreation.year)
		wikicode += "* " + dateofcreationhuman + u": [[" + page.replace('_', ' ') + u"]]\n"
	portalpage = pywikibot.Page(site, portal)
	portalpage.text = wikicode
	portalpage.save("Robot: Aktualizace novinek")
