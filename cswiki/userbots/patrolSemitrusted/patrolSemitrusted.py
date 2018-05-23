# -*- coding: utf-8 -*-

from sseclient import SSEClient as EventSource
import os
import json
import requests
import pywikibot
import logging

stream = 'https://stream.wikimedia.org/v2/stream/recentchange'

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolSemitrusted.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		site = pywikibot.Site()
		for event in EventSource(stream):
			if event.event == 'message':
				try:
					change = json.loads(event.data)
				except ValueError:
					continue
				if change['wiki'] == 'cswiki':
					if 'patrolled' not in change or change['patrolled']:
						continue
					users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolSemitrusted/users.txt', encoding="utf-8").read().split('\n')
					if 'revision' in change:
						if change['user'] in users:
							logging.info('Making %s as patrolled', change['id'])
							logging.debug('Revision data=%s', change)
							list(site.patrol(rcid=change['id']))
						else:
							logging.debug('Skipping %s', change['id'])
							logging.debug('Revision data=%s', change)
	except Exception as e:
		logging.exception('Unknown exception occured')
