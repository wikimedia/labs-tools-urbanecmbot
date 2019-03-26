# -*- coding: utf-8 -*-

from sseclient import SSEClient as EventSource
import os
import json
import requests
import pywikibot
import logging

stream = 'https://stream.wikimedia.org/v2/stream/recentchange'

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolTrusted.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
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
					if 'revision' in change:
						logging.info("Processing change %s", json.dumps(change))
						editpatrol = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt', encoding="utf-8").read().split('\n')
						autopatrol = open('/data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/pagepatrol.txt', encoding="utf-8").read().split('\n')
						if change['user'] in editpatrol and change['length']['old'] != None:
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
	except Exception as e:
		logging.exception('Unknown exception occured')
