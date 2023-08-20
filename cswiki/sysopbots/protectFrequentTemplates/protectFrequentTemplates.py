#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import mwparserfromhell
import toolforge

NS_TEMPLATE = 10
NS_MODULE = 828

PROTECTION_TEMPLATES = {
	'autoconfirmed': 'Polozamčeno',
	'extendedconfirmed': 'Rozšířeně polozamčeno',
	'sysop': 'Zamčeno'
}


def rreplace(s, old, new, occurrence):
	# comes from https://stackoverflow.com/a/2556252
	li = s.rsplit(old, occurrence)
	return new.join(li)


def add_docs_page(site, page, protection_level):
	page_namespace = page.namespace().id
	if page_namespace == NS_TEMPLATE:
		doc_page = page
	elif page_namespace == NS_MODULE:
		doc_page = pywikibot.Page(site, '%s/Dokumentace' % page.title())
	else:
		return

	code = mwparserfromhell.parse(doc_page.text)
	replaced_template = False
	new_protection_template = '{{%s}}' % PROTECTION_TEMPLATES[protection_level]
	for template in code.filter_templates():
		for _, protection_template in PROTECTION_TEMPLATES.items():
			if template.name.matches(protection_template):
				code.replace(template, new_protection_template)
				doc_page.text = str(code)
				replaced_template = True
				break

		if replaced_template:
				break

	if not replaced_template:
		if page_namespace == NS_TEMPLATE:
			if 'noinclude' in doc_page.text:
				doc_page.text = rreplace(doc_page.text, '<noinclude>', '<noinclude>%s' % new_protection_template, 1)
			else:
				doc_page.text += '<noinclude>%s</noinclude>' % new_protection_template
		elif page_namespace == NS_MODULE:
			if doc_page.exists():
				if 'includeonly' in doc_page.text:
					doc_page.text = rreplace(doc_page.text, '<includeonly>', '<includeonly>\n%s' % new_protection_template, 1)
				else:
					doc_page.text = '<includeonly>%s</includeonly>' % protection_template + '\n' + doc_page.text

	doc_page.save('Robot: Přidání šablony %s' % new_protection_template)


conn = toolforge.connect('cswiki', cluster='analytics')

with conn.cursor() as cur:
	cur.execute('''WITH highly_used_templates AS (
		SELECT
			lt_namespace,
			lt_title,
			pr_level,
			COUNT(*) AS usages
		FROM templatelinks
		JOIN linktarget ON lt_id=tl_target_id
		JOIN page ON ((lt_namespace=page_namespace) AND (lt_title=page_title))
		LEFT JOIN page_restrictions ON ((pr_type='edit') AND (page_id=pr_page))
		WHERE
				page_id IS NOT NULL
			AND page_is_redirect = 0
		GROUP BY lt_namespace, lt_title
		ORDER BY COUNT(*) DESC
	),

	new_levels_calculated AS (
		SELECT
			lt_namespace,
			lt_title,
			pr_level,
			CASE
				WHEN usages >= 5000 THEN 'extendedconfirmed'
				WHEN usages >= 2500 THEN 'extendedconfirmed'
				WHEN usages >= 250 THEN 'autoconfirmed'
				ELSE NULL
			END AS new_level,
			usages
		FROM highly_used_templates
	)

	SELECT *
	FROM new_levels_calculated
	WHERE
			pr_level IS NULL
		OR (pr_level = 'autoconfirmed' AND new_level IN ('extendedconfirmed', 'sysop'))
		OR (pr_level = 'extendedconfirmed' AND new_level = 'sysop')
	''')
	data = cur.fetchall()

site = pywikibot.Site()
for row in data:
	print(row)
	page_namespace = row[0]
	page_title = row[1].decode('utf-8')
	protection_level = row[3]
	usages = row[4]

	if protection_level is None:
		print('All templates with 250+ are protected, aborting.')
		break

	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])

	page.protect(protections={'edit': protection_level, 'move': protection_level}, reason='velmi často používaná stránka <!-- %d použití -->' % usages)

	add_docs_page(site, page, protection_level)
