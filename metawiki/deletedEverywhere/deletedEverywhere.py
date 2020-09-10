#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot

site = pywikibot.Site('meta', 'meta')

conn = toolforge.connect('wikidatawiki')
with conn.cursor() as cur:
	cur.execute('select ips_site_id, ips_site_page from wb_items_per_site where ips_item_id=5964 order by ips_site_id')
	speedy_items = cur.fetchall()

conn = toolforge.connect('centralauth')
with conn.cursor() as cur:
	cur.execute('select ws_wikis from wikiset where ws_id=7')
	non_gs_wikis = cur.fetchall()[0][0].decode('utf-8').split(',')

result = """{| class="wikitable sortable"
|+
!Project
!Number of sysops
!Link to category
!Number of items
"""

totalCSD = 0
for speedy_item in speedy_items:
	dbname = speedy_item[0].decode('utf-8')
	conn = toolforge.connect(dbname)
	with conn.cursor() as cur:
		cur.execute('select count(*) from categorylinks where cl_to=%s', speedy_item[1].decode('utf-8').split(':')[1].replace(' ', '_'))
		numOfItems = cur.fetchall()[0][0]
	with conn.cursor() as cur:
		cur.execute('select count(*) from user_groups where ug_group="sysop";')
		numOfSysops = cur.fetchall()[0][0]
	conn = toolforge.connect('meta')
	with conn.cursor() as cur:
		cur.execute('select url from wiki where dbname=%s', speedy_item[0].decode('utf-8'))
		url = cur.fetchall()[0][0]
	if dbname in non_gs_wikis:
		result += "|-\n"
	else:
		result += '|- style="background-color: #BBFFBB;"\n'
	result += "|%s\n" % speedy_item[0].decode('utf-8')
	result += "|{{subst:formatnum:%d}}\n" % numOfSysops
	result += "|[%s/wiki/%s %s]\n" % (url, speedy_item[1].decode('utf-8').replace(' ', '_'), speedy_item[1].decode('utf-8'))
	result += "|{{subst:formatnum:%d}}\n" % numOfItems
	totalCSD += numOfItems

result += """|+
! colspan="3" |Total
!{{subst:formatnum:%d}}
""" % totalCSD
result += "|}"

page = pywikibot.Page(site, "Global sysops/Speedy delete requests/Data")
page.text = result
page.save('Bot: Publish wiki speedy delete report')
