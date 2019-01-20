#!/usr/bin/env python
#-*- coding: utf-8 -*-

import os
from wmflabs import db
conn = db.connect('cswiki')

chars = {'—': '-', '…': '...'}
#Generate SQLs
sqls = []
for char in chars:
	sqls.append('select replace(page_title, "' + char + '", "' + chars[char] + '"), page_title from page where page_title like "%' + char + '%" and replace(page_title, "' + char + '", "' + chars[char] + '") not in (select page_title from page) and page_namespace=0 and page_is_redirect=0;')

#And fetch data...
data = []
for sql in sqls:
	cur = conn.cursor()
	with cur:
		cur.execute(sql)
		d = cur.fetchall()
	for row in d:
		data.append(row)

#Create file with cmds
f = open("/tmp/pywikibotToCreate_Urbanecm.txt", 'w')
for row in data:
	f.write('{{-start-}}\n')
	f.write("'''" + row[0] + "'''\n")
	f.write('#REDIRECT [[' + row[1] + ']]\n')
	f.write('{{-stop-}}\n\n')
f.close()

print "python ~/pwb/scripts/pagefromfile.py -notitle -file:'/tmp/pywikibotToCreate_Urbanecm.txt' -summary:'Robot: Přidání redirectu'"
print "rm /tmp/pywikibotToCreate_Urbanecm.txt"
