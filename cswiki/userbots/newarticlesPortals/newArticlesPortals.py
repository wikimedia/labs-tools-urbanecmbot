#!/usr/bin/env python
# coding=utf-8

# Imports
import requests
import csv
import pywikibot
import datetime
import toolforge
import simplejson as json

# Init
site = pywikibot.Site()
conn = toolforge.connect('cswiki')

# Config
CONFIG_PAGE = "Wikipedista:UrbanecmBot/Nové články na portálech.json"
config = json.loads(pywikibot.Page(site, CONFIG_PAGE).text)

BASEURL = 'https://petscan.wmflabs.org/'
BASESQL = 'select left(rev_timestamp, 8) from revision where rev_page in (select page_id from page where page_title=%s and page_namespace=0) and rev_parent_id=0;'

# Code
for portal in config['portals']:
	portal_config = {**config['defaults'], **config['portals'][portal]}
	pages = {}
	payload = {
		'language': 'cs',
		'project': 'wikipedia',
		'depth': portal_config['depth'],
		'combination': 'union',
		'categories': '\n'.join(portal_config['categories']),
		'negcats': '\n'.join(portal_config['negative_categories']),
		'ns[0]': 1,
		'after': (datetime.date.today() - datetime.timedelta(days=portal_config['before_days'])).strftime('%Y%m%d'),
		'only_new': 'on',
		'sortorder': 'descending',
		'sortby': 'none',
		"output_limit": portal_config["output_limit"],
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
	portalpage = pywikibot.Page(site, portal_config.get('target_page', 'Portál:%s/Nové články' % portal))
	portalpage.text = wikicode
	portalpage.save("Robot: Aktualizace novinek")
