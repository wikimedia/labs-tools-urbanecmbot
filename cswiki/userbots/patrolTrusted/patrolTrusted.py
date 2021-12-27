# -*- coding: utf-8 -*-

from pywikibot.comms.eventstreams import EventStreams
import os
import json
import requests
import pywikibot
import logging

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolTrusted.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		site = pywikibot.Site()
		stream = EventStreams(streams=['recentchange'])
		stream.register_filter(server_name='cs.wikipedia.org', type='edit')
		while True:
			change = next(iter(stream))
			if 'patrolled' not in change or change['patrolled']:
				continue
			if 'revision' in change:
				logging.info("Processing change %s", json.dumps(change))
				editpatrol = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt', encoding="utf-8").read().split('\n')
				autopatrol = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/pagepatrol.txt', encoding="utf-8").read().split('\n')
				if change['user'] in editpatrol and 'old' in change['length']:
					logging.info('Marking %s as patrolled, because it was made by editpatrol', change['id'])
					list(site.patrol(rcid=change['id']))
				elif change['user'] in autopatrol:
					logging.info('Marking %s as patrolled, because it was made by manual autopatrol', change['id'])
					list(site.patrol(rcid=change['id']))
				elif change['comment'].startswith('([[:c:GR|GR]])'):
					logging.info('Marking %s as patrolled, because it is a part of global rename coming from Commons', change['id'])
					list(site.patrol(rcid=change['id']))
				elif '([[Commons:Commons:GlobalReplace|' in change['comment']:
					logging.info('Marking %s as patrolled, because it is a part of global replace coming from Commons user', change['id'])
					list(site.patrol(rcid=change['id']))
	except Exception:
		logging.exception('Unknown exception occured')
