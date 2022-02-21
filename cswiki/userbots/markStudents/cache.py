#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import requests
import urllib
import pywikibot
from lxml import html
import shutil
import os

requests.utils.default_user_agent = lambda: "Dashboard Scrapper (no website exists, martin.urbanec@wikimedia.cz, https://meta.wikimedia.org/wiki/User:Martin_Urbanec)"

base = "https://outreachdashboard.wmflabs.org/campaigns/"
site = pywikibot.Site()

campaigns = [
	'studenti',
	'seniori',
	'knihovny',
]

# Clean data
if os.path.isdir('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data'):
	shutil.rmtree('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data')
os.mkdir('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data')
open('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data/.gitkeep', 'w').write('')

# Regenerate files campaign-users.txt in public iface
rules = []
conn = toolforge.connect('cswiki')
autopatrolled = []
with conn.cursor() as cur:
	sql = "select user_name from user where user_id in (select ug_user from user_groups where ug_group='autopatrolled');"
	cur.execute(sql)
	data = cur.fetchall()
	for row in data:
		autopatrolled.append(row[0].decode('utf-8'))
for campaign in campaigns:
	url = base + campaign + '/users'
	r = requests.get(url)
	tree = html.fromstring(r.content)
	users_raw = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
	users = []
	for user in users_raw:
		user = str(user)
		user = user.encode('latin1').decode('utf-8')
		if user in autopatrolled:
			continue
		users.append(user)
	f = open('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data/' + campaign + '-users.txt', 'w')
	users = list(set(users))
	users.sort()
	f.write("\n".join(users))
	f.close()
	f = open('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data/' + campaign + '-users.txt', 'r')
	page = pywikibot.Page(site, "Wikipedista:UrbanecmBot/Zvýrazňování studentů/%s-users.txt" % campaign)
	page.text = f.read()
	page.save('Robot: Aktualizace seznamu studentů')
	f.close()
	for user in users:
		rules.append("a[href$='wiki/Wikipedista:" + urllib.parse.quote(user.replace(' ', '_')) + "']")
		rules.append("a[href$='Wikipedista:" + urllib.parse.quote(user.replace(' ', '_')) + "&action=edit&redlink=1']")
		rules.append("a[href$='wiki/Wikipedistka:" + urllib.parse.quote(user.replace(' ', '_')) + "']")
		rules.append("a[href$='Wikipedistka:" + urllib.parse.quote(user.replace(' ', '_')) + "&action=edit&redlink=1']")
		rules.append("a[href$='wiki/Wikipedista:" + user.replace(' ', '_') + "']")
		rules.append("a[href$='Wikipedista:" + user.replace(' ', '_') + "&action=edit&redlink=1']")
		rules.append("a[href$='wiki/Wikipedistka:" + user.replace(' ', '_') + "']")
		rules.append("a[href$='Wikipedistka:" + user.replace(' ', '_') + "&action=edit&redlink=1']")

fcss = open('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data/stylesheet.css', 'w+')
fcss.write('@charset "utf-8";\n\n')
fcss.write(",\n".join(rules))
fcss.write("\n{ color: green !important; font-weight: bold !important; }\n\n")
fcss.close()
fcss = open('/data/project/urbanecmbot/11bots/cswiki/userbots/markStudents/data/stylesheet.css', 'r+')
page = pywikibot.Page(site, "Wikipedista:UrbanecmBot/Zvýrazňování studentů/stylesheet.css")
page.text = fcss.read()
page.save('Robot: Aktualizace CSS pravidel pro zvýrazňování')
fcss.close()
