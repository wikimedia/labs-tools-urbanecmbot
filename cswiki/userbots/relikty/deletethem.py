#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
conn = toolforge.connect('cswiki')
import pywikibot
site = pywikibot.Site()
import requests


params = {
	"action": "query",
	"format": "json",
	"meta": "siteinfo",
	"siprop": "namespaces"
}

cur = conn.cursor()
with cur:
	sql = 'select page_namespace, page_title from page where page_is_redirect=1 and (page_namespace in (14) or page_namespace%2=1) and page_namespace not in (3, 5)'
	cur.execute(sql)
	data = cur.fetchall()

for row in data:
	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])
	page.delete(reason=u"Robot: Relikt po přesunu", mark=True)
