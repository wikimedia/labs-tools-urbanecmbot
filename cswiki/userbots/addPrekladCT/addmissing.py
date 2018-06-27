#!/usr/bin/env python
#-*- coding: utf-8 -*-

from pywikibot import textlib
import re
import pywikibot
site = pywikibot.Site()


exceptions = ['comment', 'nowiki', 'pre']

rows = open('preklads.txt', 'r').read().split('\n')
for row in rows:
	row = row.split('\t')
	page = pywikibot.Page(site, row[0])
	if re.search(r'(?i)== *Reference *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)==(=?) *Reference *===?\s*', r'==\1 Reference ==\1\n' + row[1] + r'\n', exceptions)
	elif re.search(r'(?i)== *Poznámky *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)==(=?) *Poznámky *===?\s+(.*)\s*', r'==\1 Poznámky ==\1\n\2\n\n==\1 Reference ==\1\n' + row[1] + r'\n\n', exceptions)
	elif re.search(r'(?i)== *(Literatura|Související články|Externí odkazy) *==', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*==(=?) *(Literatura|Související články|Externí odkazy) *===?', r'\n\n==\1 Reference ==\1\n' + row[1] + r'\n\n==\1 \2 ==\1', exceptions, count=1)
	elif re.search(r'(?i)\{\{(Autoritní data|Portály|DEFAULTSORT)[^\}]*\}\}', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*\{\{((Autoritní data|Portály|DEFAULTSORT)[^\}]*)\}\}', r'\n\n== Reference ==\n' + row[1] + r'\n\n{{\1}}', exceptions, count=1)
	elif re.search(r'(?i)\[\[Kategorie:[^\]]*\]\]', page.text):
		page.text = textlib.replaceExcept(page.text, r'(?i)\s*\[\[Kategorie:([^\]]*)\]\]', r'\n\n== Reference ==\n' + row[1] + r'\n\n[[Kategorie:\1]]', exceptions, count=1)
	else:
		page.text = page.text + '\n\n== Reference ==\n' + row[1]
	page.save('Robot: Přidání šablony Překlad')
