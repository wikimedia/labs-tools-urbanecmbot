#!/usr/bin/env python
#-*- coding: utf-8 -*-

import HTML
import os
import cgi
import sys
from wmflabs import db

#Print header
print 'Content-type: text/html\n'

#Print header of html document
print """
<!DOCTYPE html>
<html lang="cs-cz">
        <head>
                <meta charset="utf-8" />
                <title>Relikty</title>
        </head>
        <body>
"""

#Init params

if 'QUERY_STRING' in os.environ:
        QS = os.environ['QUERY_STRING']
        qs = cgi.parse_qs(QS)
	try:
		lang = qs['lang'][0]
	except:
		lang = "cs"
	try:
		family = qs['family'][0]
	except:
		family = 'wiki'
	try:
		onlySqlSource = qs['onlysql'][0]
		if onlySqlSource == '1':
			onlySql = True
		else:
			onlySql = False
	except:
		onlySql = False
else:
	lang = "cs"
	family = "wiki"
	onlySql = False

dbname = lang + family

conn = db.connect(dbname)

cur = conn.cursor()
with cur:
	sql = 'select CONCAT(\'<a href="https://' + lang + '.wikipedia.org/w/?redirect=no&curid=\', page_id, \'">\', "https://' + lang + '.wikipedia.org/w/?redirect=no&curid=", page_id, "</a>") as url, CONCAT(\'<a href="https://' + lang + '.wikipedia.org/w/?redirect=no&curid=\',page_id,\'&action=delete">Smazat</a>\') as dellink from page where page_is_redirect=1 and (page_namespace in (14) or page_namespace%2=1) and page_namespace not in (3, 5)'
	if onlySql:
		print '<pre>'
		print sql
		print '</pre>'
		sys.exit(0)
	cur.execute(sql)
	data = cur.fetchall()

table = HTML.table(data, header_row=['URL', 'Smazat'])
print table
