#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
site = pywikibot.Site()

page = pywikibot.Page(site, 'Wikipedista:UrbanecmBot/EditPatrol')
users = page.text.split('\n')
users.pop(0)
users.pop()
users.sort()
page.text = '<pre>\n' + '\n'.join(users) + '\n</pre>'
page.save('Robot: Seřazení seznamu')
