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
	logging.basicConfig(filename='/data/project/urbanecmbot/logs/patrolAfterPatrol.log', level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')
	try:
		site = pywikibot.Site()
		for event in EventSource(stream):
			if event.event == 'message':
				try:
					change = json.loads(event.data)
				except ValueError:
					continue
				if change['wiki'] == 'cswiki':
					if 'log_type' not in change:
						continue
					if change['log_type'] == "patrol" and change["log_params"]["previd"] == "0":
						logging.info("Processing patrol action id %s", change['log_id'])
						conn = toolforge.connect('cswiki', cluster='analytics')
						with conn.cursor() as cur:
							cur.execute('select rc_id from recentchanges join revision on rev_id=rc_this_oldid where rev_page=(select log_page from logging where log_id=%s) and rc_patrolled=0 and rc_new=0;', change['log_id'])
							data = cur.fetchall()
						for row in data:
							logging.info("Marking revision %s as patrolled", int(row[0]))
							list(site.patrol(rcid=int(row[0])))
	except Exception:
		logging.exception('Unknown error occured')
