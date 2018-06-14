#!/usr/bin/env python3
#-*- coding: utf-8 -*-
import pywikibot
site = pywikibot.Site('cs', 'wikipedia')
page = pywikibot.Page(site, u"Wikipedista:UrbanecmBot/EditPatrol")
open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt', 'w').write(page.text)
