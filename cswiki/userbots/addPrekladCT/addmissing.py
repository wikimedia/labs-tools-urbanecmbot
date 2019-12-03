#!/usr/bin/env python
#-*- coding: utf-8 -*-

import toolforge
from pywikibot import textlib
import re
import pywikibot
conn = toolforge.connect('cswiki')
site = pywikibot.Site()


exceptions = ['comment', 'nowiki', 'pre']

# Get on wiki exeptions
not_edit_page = pywikibot.Page(site, u'Wikipedista:UrbanecmBot/Nepřidávat šablonu překlad')
not_edit_pages = not_edit_page.linkedPages()
not_edit = []
for page in not_edit_pages:
	not_edit.append(page.title().replace(u' ', u'_'))

# Get pages with no translation template
with conn.cursor() as cur:
	cur.execute(open('sql.sql').read())
	data = cur.fetchall()

for row in data:
	if row[0].decode('utf-8') in not_edit:
		print('Skipping %s' % row[0].decode('utf-8'))
		continue # Skip page if in exeptions
	page = pywikibot.Page(site, row[0].decode('utf-8'))
	if '{{překlad' in page.text.lower():
		continue # Skip page if contain translation template
	if re.search(r'(?i)== *Reference *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)==(=?) *Reference *===?\s*', r'==\1 Reference ==\1\n' + row[1].decode('utf-8') + r'\n', exceptions)
	elif re.search(r'(?i)== *Poznámky *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)==(=?) *Poznámky *===?\s+(.*)\s*', r'==\1 Poznámky ==\1\n\2\n\n==\1 Reference ==\1\n' + row[1].decode('utf-8') + r'\n\n', exceptions)
	elif re.search(r'(?i)== *(Literatura|Související články|Externí odkazy) *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*==(=?) *(Literatura|Související články|Externí odkazy) *===?', r'\n\n==\1 Reference ==\1\n' + row[1].decode('utf-8') + r'\n\n==\1 \2 ==\1', exceptions, count=1)
	elif re.search(r'(?i)\{\{(Autoritní data|Portály|DEFAULTSORT)[^\}]*\}\}', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*\{\{((Autoritní data|Portály|DEFAULTSORT)[^\}]*)\}\}', r'\n\n== Reference ==\n' + row[1].decode('utf-8') + r'\n\n{{\1}}', exceptions, count=1)
	elif re.search(r'(?i)\[\[Kategorie:[^\]]*\]\]', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*\[\[Kategorie:([^\]]*)\]\]', r'\n\n== Reference ==\n' + row[1].decode('utf-8') + r'\n\n[[Kategorie:\1]]', exceptions, count=1)
	else:
		page.text = page.text + '\n\n== Reference ==\n' + row[1].decode('utf-8')
	try:
		page.save('Robot: Přidání šablony Překlad')
	except Exception:
		pass
