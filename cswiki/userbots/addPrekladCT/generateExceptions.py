#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot

site = pywikibot.Site()
definition = pywikibot.Page(site, u'Wikipedista:UrbanecmBot/Nepřidávat šablonu překlad')

exceptions = definition.linkedPages()

for page in exceptions:
	print(page.title().replace(u' ', u'_'))
