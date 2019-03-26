# -*- coding: utf-8 -*-

from sseclient import SSEClient as EventSource
import os
import json
import requests
import pywikibot
import logging
import toolforge

stream = 'https://stream.wikimedia.org/v2/stream/recentchange'

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolSandbox.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		site = pywikibot.Site()
		for event in EventSource(stream):
			if event.event == 'message':
				try:
					change = json.loads(event.data)
				except ValueError:
					continue
				if change['wiki'] == 'cswiki' and 'revision' in change and not change['patrolled']:
					logging.info("Processing change %s", json.dumps(change))
					if change["title"].startswith("Wikipedista:%s" % change['user']) and 'old' not in change['length']:
						logging.info('Marking %s as patrolled, because it was made in personal user space', change['id'])
						list(site.patrol(rcid=change['id']))
	except Exception as e:
		logging.exception('Unknown error occured')
