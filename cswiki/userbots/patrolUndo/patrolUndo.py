#!/usr/bin/python
# -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0
import logging
import pywikibot

from datetime import timedelta, datetime

logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolUndo.log',
		    level=logging.DEBUG,
		    format='%(asctime)s %(levelname)s:%(message)s')

args = pywikibot.handle_args()

site = pywikibot.Site()

minutes = int(args[0]) if args and args[0].isdigit() else 15

start = datetime.utcnow() - timedelta(minutes=minutes)
starttime = start.strftime('%Y%m%d%H%M%S')

for rev in site.recentchanges(
        start=starttime, showBot=False, showPatrolled=True, reverse=True,
        tag='mw-undo'):
    try:
	p = site.patrol(revid=rev['old_revid'])
	list(p)
	logging.info('Marking revision %s as patrolled', rev['old_revid'])
    except Exception as e:
        logging.exception('Exception occured')
