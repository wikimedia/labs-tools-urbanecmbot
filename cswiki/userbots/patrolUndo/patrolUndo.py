#!/usr/bin/python
# -*- coding: UTF-8 -*-
# licensed under CC-Zero: https://creativecommons.org/publicdomain/zero/1.0

import pywikibot
from datetime import timedelta, datetime
import logging

logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolUndo.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')

start = datetime.today() - timedelta(minutes=15)
starttime = start.strftime('%Y%m%d%H%M%S')

site = pywikibot.Site('cs', 'wikipedia')

for rev in site.recentchanges(start=starttime, showBot=False, showPatrolled=True, reverse=True):
    try:
        if 'mw-undo' in rev['tags']:
            p = site.patrol(revid=rev['revid'])
            next(p)
	    logging.info('Marking revision revid %s as patrolled', rev['revid'])
    except Exception as e:
        logging.exception('Exception occured')
