#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()

ids = open('topatrol.txt').readlines()

for id in ids:
	id = int(id.replace('\n', ''))
	try:
		list(site.patrol(rcid=id))
	except:
		pass
