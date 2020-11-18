#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot
import urllib

conn = toolforge.connect('cswiki')
site = pywikibot.Site()
page = pywikibot.Page(site, "User:UrbanecmBot/Zývrazňování loutek.css")

with conn.cursor() as cur:
	cur.execute('select page_title from categorylinks join page on page_id=cl_from where cl_to="Wikipedie:Podezřelé_loutkové_účty" and page_namespace=2')
	data = cur.fetchall()

rules = []
for row in data:
	title = row[0].decode('utf-8')
	title_encoded = urllib.parse.quote(title).replace(' ', '_')
	rules.append("a[href$='wiki/Wikipedista:%s']" % title_encoded)
	rules.append("a[href$='Wikipedista:%s']" % title_encoded)
	rules.append("a[href$='wiki/Wikipedistka:%s']" % title_encoded)
	rules.append("a[href$='Wikipedistka:%s']" % title_encoded)

css = '@charset "utf-8";\n\n'
css += ",\n".join(rules)
css += "\n{ color: grey !important; text-decoration: line-through !important; }\n"
page.text = css
page.save('Robot: Aktualizace CSS stylopisu')
