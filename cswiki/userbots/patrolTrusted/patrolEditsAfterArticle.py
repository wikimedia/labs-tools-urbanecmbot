# -*- coding: utf-8 -*-

from sseclient import SSEClient as EventSource
import os
import json
import requests
import pywikibot
import logging
import toolforge

from threading import Thread
from queue import Queue

def work(queue):
	site = pywikibot.Site()
	conn = toolforge.connect('cswiki', cluster='analytics')
	while True:
		log_id = queue.get()
		if log_id is None:
			break
		with conn.cursor() as cur:
			cur.execute('select rc_id from recentchanges join revision on rev_id=rc_this_oldid where rev_page=(select log_page from logging where log_id=%s) and rc_patrolled=0 and rc_new=0;', log_id)
			data = cur.fetchall()
		for row in data:
			logging.info("Marking revision %s as patrolled", int(row[0]))
			list(site.patrol(rcid=int(row[0])))


stream = 'https://stream.wikimedia.org/v2/stream/recentchange'
queue = Queue()
thread = Thread(target=work, args=[queue])
thread.start()

if __name__ == "__main__":
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolAfterPatrol.log', level=logging.DEBUG, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		for event in EventSource(stream):
			if event.event == 'message':
				try:
					change = json.loads(event.data)
				except ValueError:
					continue
				if change['wiki'] == 'cswiki':
					if change.get('log_type') == 'patrol' and change['log_params']['previd'] == '0':
						queue.put(change['log_id'])
	except Exception as e:
		logging.exception('Unknown error occured')
		queue.put(None)
		thread.join()
