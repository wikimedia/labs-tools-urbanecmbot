#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

NS_TEMPLATE = 10
NS_MODULE = 828

PROTECTION_TEMPLATES = {
	'autoconfirmed': '{{polozamčeno}}',
	'extendedconfirmed': '{{rozšířeně polozamčeno}}',
	'sysop': '{{zamčeno}}'
}


def rreplace(s, old, new, occurrence):
	# comes from https://stackoverflow.com/a/2556252
	li = s.rsplit(old, occurrence)
	return new.join(li)


conn = toolforge.connect('cswiki', cluster='analytics')

with conn.cursor() as cur:
	cur.execute("select lt_namespace, lt_title, pr_level, count(*) from templatelinks join linktarget on lt_id=tl_target_id left join page on ((lt_namespace=page_namespace) and (lt_title=page_title)) left join page_restrictions on ((pr_type='edit') and (page_id=pr_page)) where page_id is not null and pr_level is null and page_is_redirect=0 group by lt_namespace, lt_title order by count(*) desc")
	data = cur.fetchall()

site = pywikibot.Site()
for row in data:
	print(row)
	page_namespace = row[0]
	page_title = row[1].decode('utf-8')
	usages = row[3]

	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])

	# determine protection level
	protection_level = None
	if usages >= 5000:
		protection_level = 'sysop'
	elif usages >= 2500:
		protection_level = 'extendedconfirmed'
	elif usages >= 250:
		protection_level = 'autoconfirmed'

	if protection_level is None:
		print('All templates with 250+ are protected, aborting.')
		break

	page.protect(protections={'edit': protection_level, 'move': protection_level}, reason='velmi často používaná stránka <!-- %d použití -->' % usages)

	protection_template = PROTECTION_TEMPLATES[protection_level]
	if page_namespace == NS_TEMPLATE:
		if 'noinclude' in page.text:
			page.text = rreplace(page.text, '<noinclude>', '<noinclude>%s' % protection_template, 1)
		else:
			page.text += '<noinclude>%s</noinclude>' % protection_template

		page.save('Robot: Přidání šablony %s' % protection_template)
	elif page_namespace == NS_MODULE:
		doc_page = pywikibot.Page(site, '%s/Dokumentace' % page.title())
		if doc_page.exists():
			doc_page.text = '<includeonly>%s</includeonly>' % protection_template + '\n' + doc_page.text
			doc_page.save('Robot: Přidání šablony %s' % protection_template)
