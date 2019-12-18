#!/usr/bin/env python
# coding=utf-8

# Imports
import requests
import csv
import pywikibot
import datetime
from wmflabs import db

# Config
DEPTH = 5
PORTALS = {
	u'Portál:Ptáci/Nové články': 'Ptáci',
	u'Portál:Obojživelníci/Nové články': 'Obojživelníci'
}
EXCEPTIONS = {
	'SOME': ['SOME']
}
BASEURL = 'https://petscan.wmflabs.org/'
BASESQL = 'select left(rev_timestamp, 8) from revision where rev_page in (select page_id from page where page_title="@@TITLE@@" and page_namespace=0) and rev_parent_id=0;'

BEFORE_DAYS = 30

AFTER_DATE = (datetime.date.today() - datetime.timedelta(days=BEFORE_DAYS)).strftime('%Y%m%d')

# Code
conn = db.connect('cswiki')
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
			sql = BASESQL.replace('@@TITLE@@', page['title'])
			cur.execute(sql)
			dayofcreation = cur.fetchall()[0][0]
		pages[dayofcreation] = page['title']
	dateofcreations = pages.keys()
	dateofcreations.sort()
	wikicode = u"<!-- Prosím, nepřepisujte tuto stránku, příští noc budou změny přepsány botem -->\n\n"
	for dateofcreationraw in dateofcreations:
		page = pages[dateofcreationraw]
		dateofcreation = datetime.datetime.strptime(dateofcreationraw, '%Y%m%d')
		dateofcreationhuman = "{0}. {1}. {2}".format(dateofcreation.day, dateofcreation.month, dateofcreation.year)
		wikicode += u"* " + dateofcreationhuman + u": [[" + page.replace('_', ' ') + u"]]\n"
	portalpage = pywikibot.Page(site, portal)
	portalpage.text = wikicode
	portalpage.save(u"Robot: Aktualizace novinek")
	break
