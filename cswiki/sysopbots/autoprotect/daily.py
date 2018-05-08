#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import datetime

site = pywikibot.Site()

monthword = {
	1: u"leden",
	2: u"únor",
	3: u"březen",
	4: u"duben",
	5: u"květen",
	6: u"červen",
	7: u"červenec",
	8: u"srpen",
	9: u"září",
	10: u"říjen",
	11: u"listopad",
	12: u"prosinec"
}
d = datetime.date.today()
day = d.day
month = monthword[d.month]
page_title = u"Wikipedie:Vybraná výročí dne/%d. %s" % (day, month)
page = pywikibot.Page(site, page_title)
page.protect(reason='automatizovany zamek neceho dne', protections={'edit': 'autoconfirmed', 'move': 'sysop'}, expiry="26 hours")
