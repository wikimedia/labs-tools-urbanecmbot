#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site('meta', 'meta')

for page_title in ["Merchandise giveaways/——————————"]:
	page = pywikibot.Page(site, page_title)
	page.touch()
