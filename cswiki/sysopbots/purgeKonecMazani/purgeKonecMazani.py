#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()

for page_title in ["MediaWiki:Konec mazání", "Wikipedie:Porušení práv/Články zřejmě porušující autorská práva/Copyvia"]:
	page = pywikibot.Page(site, page_title)
	page.touch()
