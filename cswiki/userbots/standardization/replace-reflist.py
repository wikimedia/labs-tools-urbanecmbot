#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import mwparserfromhell
import toolforge

conn = toolforge.connect('cswiki')
with conn.cursor() as cur:
	cur.execute("select page_namespace, page_title from templatelinks join linktarget on lt_id=tl_target_id join page on page_id=tl_from where tl_from_namespace=0 and lt_namespace=10 and lt_title='Reflist'")
	data = cur.fetchall()

site = pywikibot.Site('cs', 'wikipedia')
for row in data:
	page = pywikibot.Page(site, row[1].decode('utf-8'), ns=row[0])
	code = mwparserfromhell.parse(page.text)
	for template in code.filter_templates():
		if template.name.matches('Reflist'):
			refs = None
			group = None
			for param in template.params:
				if param.name.matches('refs'):
					refs = str(param.value)
				if param.name.matches('group'):
					group = str(param.value)
					if group[0] == '"':
						group = group[1:]
					if group[-1] == '"':
						group = group[:-1]

			replace_with = '<references '
			if group:
				replace_with += 'group="%s" ' % group
			if refs:
				replace_with += '>\n' + refs + '\n</references>'
			else:
				replace_with += '/>'

			code.replace(template, replace_with)

	page.text = str(code)
	page.save('Robot: Nahrazení šablony Reflist za tag <references />')
