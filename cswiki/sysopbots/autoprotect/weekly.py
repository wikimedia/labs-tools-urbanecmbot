#-*- coding: utf-8 -*-
import pywikibot
import datetime

d = datetime.date.today() + datetime.timedelta(days=5) # we want to protect day ahead
yearweek = d.isocalendar()[:2]
# ^ tohle nám dá dvojici (rok, týden)
expiry = d + datetime.timedelta(days=7)

pages = [ # různé články pro tento týden
	'Wikipedie:Článek týdne/%04d/%02d' % yearweek,
	'Wikipedie:Obrázek týdne/%04d/%02d' % yearweek,
	'Wikipedie:Zajímavosti/%04d/%02d' % yearweek,
]

site = pywikibot.Site()
for pgname in pages: # pro každou stránku ze seznamu
	page = pywikibot.Page(site, pgname) # najdu ji na wiki
	if page.exists():
		page.protect( # a zamknu...
			reason='automatizovany zamek neceho tydne', # popis editace
			protections={'edit': 'autoconfirmed', 'move': 'sysop'},
			expiry=expiry.strftime('%Y-%m-%d 07:00:00')
		)
