#-*- coding: utf-8 -*-
import pywikibot
import datetime

d = datetime.date.today()
yearweek = d.isocalendar()[:2]
# ^ tohle nám dá dvojici (rok, týden)

pages = [ # různé články pro tento týden
        u'Wikipedie:Článek týdne/%04d/%02d' % yearweek,
        u'Wikipedie:Obrázek týdne/%04d/%02d' % yearweek,
        u'Wikipedie:Zajímavosti/%04d/%02d' % yearweek,
]

site = pywikibot.getSite()
for pgname in pages: # pro každou stránku ze seznamu
        page = pywikibot.Page(site, pgname) # najdu ji na wiki
        page.protect( # a zamknu...
            reason='automatizovany zamek neceho tydne', # popis editace
	    protections={'edit': 'autoconfirmed', 'move': 'sysop'},
	    expiry='170 hours'
        )
pywikibot.stopme() # dáme prostor i ostatním
