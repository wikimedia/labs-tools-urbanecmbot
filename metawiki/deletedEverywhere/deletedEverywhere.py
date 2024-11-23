#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot
import requests
from datetime import datetime

site = pywikibot.Site('meta', 'meta')

conn = toolforge.connect('wikidatawiki')
with conn.cursor() as cur:
	cur.execute('select ips_site_id, ips_site_page from wb_items_per_site where ips_item_id=5964 order by ips_site_id')
	speedy_items = cur.fetchall()

conn = toolforge.connect('centralauth')
with conn.cursor() as cur:
	cur.execute('select ws_wikis from wikiset where ws_id=7')
	non_gs_wikis = cur.fetchall()[0][0].decode('utf-8').split(',')

s = requests.Session()
s.headers.update({'User-Agent': 'UrbanecmBot (meta.wikimedia.org; tools.urbanecmbot@tools.wmflabs.org)'})
sysopData = s.get('https://analytics.wikimedia.org/published/datasets/one-off/urbanecm/humans-by-user-group/total-users-per-group.json').json().get('sysop', {})

result = """{| class="wikitable sortable"
|+
!Project
!Number of sysops
!Link to category
!Number of items
"""
resultCSV = 'Project\tNumber of sysops\tLink to category\tNumber of items\tIs GS?\n'

totalCSD = 0
for speedy_item in speedy_items:
	dbname = speedy_item[0].decode('utf-8')
	tmp = speedy_item[1].decode('utf-8').replace(' ', '_').split(':')
	tmp.pop(0)
	cat = ":".join(tmp)

	conn = toolforge.connect('meta')
	with conn.cursor() as cur:
		cur.execute('select url, is_closed from wiki where dbname=%s', speedy_item[0].decode('utf-8'))
		data = cur.fetchall()
		if len(data) == 0:
			# wiki is not yet in toolforge's database, skipping
			continue
		url = data[0][0]
		is_closed = data[0][1]
	if is_closed:
		continue # do not process closed wikis

	conn = toolforge.connect(dbname)
	with conn.cursor() as cur:
		cur.execute('select count(*) from categorylinks where cl_to=%s', cat)
		numOfItems = cur.fetchall()[0][0]
	if numOfItems == 0:
		# nothing to delete, do not include
		continue

	numOfSysops = sysopData.get(dbname, 0)

	if dbname in non_gs_wikis:
		result += "|-\n"
	else:
		result += '|- style="background-color: #BBFFBB;"\n'
	result += "|%s\n" % speedy_item[0].decode('utf-8')
	result += "|{{subst:formatnum:%d}}\n" % numOfSysops
	result += "|[%s/wiki/%s %s]\n" % (url, speedy_item[1].decode('utf-8').replace(' ', '_'), speedy_item[1].decode('utf-8'))
	result += "|{{subst:formatnum:%d}}\n" % numOfItems
	resultCSV += '\t'.join([speedy_item[0].decode('utf-8'), str(numOfSysops), speedy_item[1].decode('utf-8'), str(numOfItems), str(dbname in non_gs_wikis)])
	totalCSD += numOfItems

with open('/data/project/urbanecmbot/public_html/deleted-everywhere/data-%s.tsv' % datetime.now().strftime('%Y%m%d%H%M%S'), 'w') as f:
	f.write(resultCSV)

result += """|+
! colspan="3" |Total
!{{subst:formatnum:%d}}
""" % totalCSD
result += "|}\n"
result += "<small>Available as TSV: [https://urbanecmbot.toolforge.org/deleted-everywhere/ download]</small>"

page = pywikibot.Page(site, "Global sysops/Speedy delete requests/Data")
page.text = result
page.save('Bot: Publish wiki speedy delete report')
