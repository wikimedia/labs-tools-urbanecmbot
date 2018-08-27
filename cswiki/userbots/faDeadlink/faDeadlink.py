#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

conn = toolforge.connect('cswiki')
site = pywikibot.Site()

with conn.cursor() as cur:
	cur.execute('select page_id, page_title from categorylinks join page on cl_from=page_id where cl_to in ("Wikipedie:Nejlepší_články", "Wikipedie:Dobré_články") and cl_type="page" and cl_from in (select cl_from from categorylinks where cl_to="Údržba:Články_obsahující_odkazy_na_nedostupné_zdroje");')
	data = cur.fetchall()

page = pywikibot.Page(site, "Wikipedie:Údržbové seznamy/Nejlepší či dobré články s nedostupnými zdroji/seznam")
page.text = ""
for row in data:
	page.text += "# [[%s]]\n" % row[1].decode('utf-8')

page.save("Robot: Aktualizace seznamu dobrých či nejlepších článnků s nedostupnými zdroji")
