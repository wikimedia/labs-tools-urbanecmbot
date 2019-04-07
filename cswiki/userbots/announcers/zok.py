# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

PAGE_PREFIX = "Wikipedie:Žádost o komentář"
PAGE_LIST = "Wikipedie:Žádost o komentář"
RE_SECTION = re.compile(r'^==[^=\n]+(|.*[^=\n]+)==\s*$', re.MULTILINE)
RE_SUBPAGE = re.compile(r'\[\[/(?P<subpage>[^\}\n]+)/\]\]')

def get_candidates(site):
	page = pywikibot.Page(site, PAGE_LIST)
	last_section = re.split(RE_SECTION, page.get())[-1]
	out = []
	for candidate in RE_SUBPAGE.finditer(last_section):
		subpage_name = candidate.group('subpage')
		out.append({
			'PREFIX': PAGE_PREFIX,
			'subpage_name': subpage_name,
		})
	return out

ANNOUNCES = [
		{'page':u'Šablona:OznámeníRC/ŽOK', 'big_tl':u'|- id="Sablona--OznameniRC__Oznameni_Diskuse"\n! [[Wikipedie:Žádost o komentář|Žádost o komentář]]:\n| %s<noinclude>{{Dlouhodobě polozamčeno}}</noinclude>', 'small_tl':u"[[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]]", 'separator':u' • ', 'empty':u'<!-- momentálně tu nic není --><noinclude>{{Dlouhodobě polozamčeno}}</noinclude>'},
		{'page':u'User:UrbanecmBot/ŽOK-PortálWP', 'big_tl':u'%s\n', 'small_tl':u"* [[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]]", 'separator':u'\n', 'empty':u'<!-- momentálně tu nic není -->'},
]

def announce_candidates(site, candidates):
	for announce in ANNOUNCES:
		if len(candidates) > 0:
			items = [announce['small_tl'] % candidate for candidate in candidates]
			inner_text = announce['separator'].join(items)
			new_text = announce['big_tl'] % inner_text
		else:
			new_text = announce['empty']
		page = pywikibot.Page(site, announce['page'])
		if not page.exists() or new_text.strip() != page.get().strip():
			comment = u'hlásič ŽOK hlásá (počet: %s)' % len(candidates)
			page.put(new_text, comment=comment)
		

if __name__ == '__main__':
	site = pywikibot.Site()
	candidates = get_candidates(site)
	announce_candidates(site, candidates)
	pywikibot.stopme()
