#!/usr/bin/env python3
#-*- coding: utf-8 -*-

import toolforge
import json
import re
import pywikibot
import mwparserfromhell

site = pywikibot.Site()
conn = toolforge.connect('cswiki')

templates = json.loads(pywikibot.Page(site, "Wikipedie:Citace/Anglické citační šablony.json").text)

template_names = []
template_names_query = []
for template in templates:
	if template != "dokumentace":
		template_names.append(template.replace('_', ' ').lower())
		template_names_query.append(template.replace(' ', '_')[0].upper() + template.replace(' ', '_')[1:].lower())

with conn.cursor() as cur:
	cur.execute('select page_title from templatelinks join page on tl_from=page_id where tl_title in (%s) and page_namespace=0 limit 1', ", ".join(template_names_query))
	data = cur.fetchall()
for row in data:
	page = pywikibot.Page(site, row[0].decode('utf-8'))

	# Preprocessing - merge parameters that shall be merged
	code = mwparserfromhell.parse(page.text)
	for template in code.filter_templates():
		template_name = template.name.lower().strip()
		if template_name in template_names:
			for param_to_merge in templates[template_name]['parameters_to_merge']:
				to_merge = []
				for param_name in param_to_merge['order']:
					for param in template.params:
						if param_name == param.name.strip():
							to_merge.append(str(param.value))
							template.remove(param.name)
				if to_merge:
					template.add(param_to_merge['order'][0], param_to_merge['delimiter'].join(to_merge))
	page.text = str(code)

	# Change the citation templates parameters blindly
	for template in templates:
		for parameter in templates[template]['parameters']:
			page.text = re.sub(r"(\{\{%s[^}]*\| *)%s( *)=" % (template, parameter), r"\1%s\2=" % templates[template]['parameters'][parameter], page.text, flags=re.IGNORECASE)
		page.text = re.sub(r"\{\{%s( *(\}\}|\|))" % template, r"{{%s\1" % templates[template]['local'], page.text, flags=re.IGNORECASE)
	page.save('Robot: Nahrazení dočasné citačních šablon za české')
