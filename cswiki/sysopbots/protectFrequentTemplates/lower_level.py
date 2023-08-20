#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
import pywikibot

conn = toolforge.connect('cswiki', cluster='analytics')
with conn.cursor() as cur:
	cur.execute('''
	WITH bot_protected_pages AS (
	    SELECT
		log_page,
		log_namespace,
		log_title,
		comment_text
	    FROM logging
	    JOIN actor ON actor_id=log_actor
	    JOIN comment on comment_id=log_comment_id
	    WHERE
		    log_type = 'protect'
		AND actor_name = 'UrbanecmSprávcoBot'
		AND log_namespace = 10
		AND comment_text LIKE 'velmi často používaná stránka%použití%'
	)

	SELECT
	    log_namespace,
	    log_title,
	    comment_text
	FROM page_restrictions
	JOIN bot_protected_pages ON pr_page = log_page
	WHERE
		pr_type = 'edit'
	    AND pr_level = 'sysop'
	''')
	data = cur.fetchall()

site = pywikibot.Site('cs', 'wikipedia')

for row in data:
	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])
	print(page.title())
	comment = row[2].decode('utf-8').replace(' -->', '; snížení úrovně per [[special:Permalink/23075639#Zamčená šablona|žádost]] -->')
	page.protect(protections={'edit': 'extendedconfirmed', 'move': 'extendedconfirmed'}, reason=comment)
	page.text = page.text.replace('{{zamčeno}}', '{{rozšířeně polozamčeno}}')
	page.save('robot: aktualizace úrovně zámku')
