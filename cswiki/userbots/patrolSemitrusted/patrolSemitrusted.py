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
					users = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolSemitrusted/users.txt').read().split('\n')
					if change['user'] in users:
						list(site.patrol(rcid=change['id']))
	except Exception as e:
		logging.exception('Unknown exception occured')
