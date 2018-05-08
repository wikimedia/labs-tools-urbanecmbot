#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()
page = pywikibot.Page(site, u"MediaWiki:Konec mazání")
page.touch()
