#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import requests
import toolforge
site = pywikibot.Site()
conn = toolforge.connect('cswiki', cluster='analytics')

params = {
	"action": "query",
	"format": "json",
	"meta": "siteinfo",
	"siprop": "namespaces"
}
r = requests.get('https://cs.wikipedia.org/w/api.php', params=params)
namespaces = r.json()['query']['namespaces']

cur = conn.cursor()
with cur:
	sql = open('/data/project/urbanecmbot/11bots/cswiki/sysopbots/orphan/sql.sql').read()
	cur.execute(sql)
	data = cur.fetchall()

exceptions = pywikibot.Page(site, "User:UrbanecmBot/Záměrně osiřelé diskusní stránky").text.split('\n')

for row in data:
	page = pywikibot.Page(site, namespaces[str(row[0])]['*'] + u':' + row[1].decode('utf-8'))
	if page.title() in exceptions:
		continue
	page.delete(reason=u"Robot: Osiřelá diskusní stránka", mark=True, prompt=False)
