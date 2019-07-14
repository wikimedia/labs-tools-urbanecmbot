#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()

for page_title in ["MediaWiki:Konec mazání"]:
	page = pywikibot.Page(site, page_title)
	page.touch()

for page_title in ["Wikipedie:Porušení práv/Články zřejmě porušující autorská práva"]:
	page = pywikibot.Page(site, page_title)
	page.purge()
