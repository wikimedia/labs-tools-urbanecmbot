# -*- coding: utf-8 -*-

from pywikibot.comms.eventstreams import EventStreams
import os
import json
import requests
import pywikibot
import logging
import toolforge

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolSandbox.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		site = pywikibot.Site()
		stream = EventStreams(streams=['recentchange'])
		stream.register_filter(server_name='cs.wikipedia.org', type='edit')
		while True:
			change = next(iter(stream))
			if 'revision' in change and not change['patrolled']:
				logging.info("Processing change %s", json.dumps(change))
				if change["title"].startswith("Wikipedista:%s" % change['user']) and 'old' in change['length']:
					logging.info('Marking %s as patrolled, because it was made in personal user space', change['id'])
					list(site.patrol(rcid=change['id']))
	except Exception:
		logging.exception('Unknown error occured')
