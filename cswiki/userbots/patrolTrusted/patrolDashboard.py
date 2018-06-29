#!/usr/bin/python
# -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0
import logging
import pywikibot

from datetime import timedelta, datetime

logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolDashboard.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

args = pywikibot.handle_args()

site = pywikibot.Site()

minutes = int(args[0]) if args and args[0].isdigit() else 15

start = datetime.utcnow() - timedelta(minutes=minutes)
starttime = start.strftime('%Y%m%d%H%M%S')

for rev in site.recentchanges(start=starttime, showBot=False, showPatrolled=False, reverse=True, tag='OAuth CID: 1024'):
	try:
		p = site.patrol(revid=rev['revid'])
		list(p)
		logging.info('Marking revision %s as patrolled', rev['revid'])
	except Exception as e:
		logging.exception('Exception occured')
