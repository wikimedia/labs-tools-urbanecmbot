#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
conn = toolforge.connect('cswiki')
import pywikibot
site = pywikibot.Site('cs', 'wikipedia')

with conn.cursor() as cur:
	cur.execute('select rc_id from recentchanges where rc_new=0 and rc_patrolled=0 and rc_comment like "([[c:GR|GR]])%";')
	data = cur.fetchall()

for row in data:
	list(site.patrol(rcid=int(row[0])))
