#!/usr/bin/env python
# coding=utf-8

# Imports
import requests
import csv
import pywikibot
import datetime
import toolforge
import time
import simplejson as json

# Init
site = pywikibot.Site()
conn = toolforge.connect('cswiki')
s = requests.Session()
s.headers.update({'User-Agent': 'User:UrbanecmBot (tools.urbanecmbot@toolforge.org)'})

# Config
CONFIG_PAGE = "Wikipedie:Automatická aktualizace nových článků portálu/konfigurace.json"
config = json.loads(pywikibot.Page(site, CONFIG_PAGE).text)

BASEURL = 'https://petscan.toolforge.org/'
BASESQL = 'select rev_timestamp from revision where rev_page in (select page_id from page where page_title=%s and page_namespace=0) and rev_parent_id=0;'

# Code
for portal in config['portals']:
	portal_config = {**config['defaults'], **config['portals'][portal]}
	print("Processing %s" % portal)
	portalpage = pywikibot.Page(site, portal_config.get('target_page', 'Portál:%s/Nové články' % portal))

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
	r = s.post(BASEURL, data=payload, allow_redirects=False)
	time.sleep(3)

	try:
		r.raise_for_status()
		if r.is_redirect:
			raise RuntimeError(f'PetScan redirected to {r.headers.get("Location")}')
		data = r.json()
	except Exception as e:
		errorMsg = repr(e)
		print(f'ERROR: Error processing {portal}: {errorMsg}')
		portalpage.text = f'CHYBA: Zpracování se nepodařilo z důvodu chyby {errorMsg}'
		portalpage.save("Robot: Aktualizace novinek se nezdařila, hlášení chyby ([[%s|nastavení]])" % CONFIG_PAGE)
		continue

	if 'error' in data:
		print('ERROR: Error processing %s, error="%s"' % (portal, data['error']))
		portalpage.text = 'CHYBA: Zpracování se nepodařilo z důvodu chyby %s' % data['error']
		portalpage.save("Robot: Aktualizace novinek se nezdařila, hlášení chyby ([[%s|nastavení]])" % CONFIG_PAGE)
		continue

	for page in data['*'][0]['a']['*']:
		with conn.cursor() as cur:
			cur.execute(BASESQL, (page['title'], ))
			dayofcreation = cur.fetchall()[0][0].decode('utf-8')
		pages[dayofcreation] = page['title']
	dateofcreations = list(pages.keys())
	dateofcreations.sort()
	if portal_config['ordering'] == 'desc':
		dateofcreations.reverse()
	wikicode = "<!-- Prosím, nepřepisujte tuto stránku, příští noc budou změny přepsány botem; nastavení najdete na [[%s]] -->\n\n" % CONFIG_PAGE
	for dateofcreationraw in dateofcreations:
		page = pages[dateofcreationraw]
		dateofcreation = datetime.datetime.strptime(dateofcreationraw, '%Y%m%d%H%M%S')
		dateofcreationhuman = "{0}. {1}. {2}".format(dateofcreation.day, dateofcreation.month, dateofcreation.year)
		wikicode += portal_config['row_format'] % {
			"date": dateofcreationhuman,
			"datetime_raw": dateofcreationraw,
			"title": page.replace('_', ' ')
		}
		wikicode += '\n'
	portalpage.text = wikicode
	portalpage.save("Robot: Aktualizace novinek dle [[%s|nastavení]]" % CONFIG_PAGE)
