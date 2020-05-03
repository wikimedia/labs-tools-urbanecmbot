#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge

conn = toolforge.connect('cswiki')

with conn.cursor() as cur:
	cur.execute('select page_title from page where page_namespace=0 and page_id not in (select pl_from from pagelinks);')
	data = cur.fetchall()

for row in data:
	with conn.cursor() as cur:
		cur.execute('select count(*) from pagelinks where pl_from=(select page_id from page where page_namespace=0 and page_title="%s");' % row[0])
		data2 = cur.fetchall()
	if data2[0][0] == 0:
		print(row[0])
