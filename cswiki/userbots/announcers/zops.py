# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

PAGE_PREFIX = "Wikipedie:Žádost o práva správce"
PAGE_LIST = "Wikipedie:Žádost o práva správce"
RE_SECTION = re.compile(r'^==[^=\n]+(|.*[^=\n]+)==\s*$', re.MULTILINE)
RE_SUBPAGE = re.compile(r'\{\{[^\}\n]*/(?P<subpage>[^\}\n]+)\}\}')
RE_CLOSE = re.compile(r"\* '''hlasování končí:''' ([0-9]+\. [0-9]+\.) [0-9]+")

def get_candidates(site):
	page = pywikibot.Page(site, PAGE_LIST)
	last_section = re.split(RE_SECTION, page.get())[-1]
	out = []
	for candidate in RE_SUBPAGE.finditer(last_section):
		subpage_name = candidate.group('subpage')
		subpage = pywikibot.Page(site, u'%s/%s' % (PAGE_PREFIX, subpage_name))
		close = RE_CLOSE.search(subpage.text)
		out.append({
			'PREFIX': PAGE_PREFIX,
			'subpage_name': subpage_name,
			'close': close.group(1),
		})
	return out

ANNOUNCES = [
	{'page':u'User:UrbanecmBot/ŽOPS-OznámeníRC', 'big_tl':u'|- id="Sablona--OznameniRC__Oznameni_Zadost-o-prava-spravce"\n! [[Wikipedie:Žádost o práva správce|Žádosti o&nbsp;práva správce]]:\n| %s\n', 'small_tl':u"[[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (%(close)s)", 'separator':u' • ', 'empty':u'<!-- momentálně tu nic není -->'},
	{'page':u'User:UrbanecmBot/ŽOPS-PortálWP', 'big_tl':u'%s\n', 'small_tl':u"* [[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (%(close)s)", 'separator':u'\n', 'empty':u'<!-- momentálně tu nic není -->'},
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
			comment = u'hlásič ŽOPS hlásá (počet: %s)' % len(candidates)
			page.put(new_text, comment=comment)
		

if __name__ == '__main__':
	site = pywikibot.Site()
	candidates = get_candidates(site)
	announce_candidates(site, candidates)
	pywikibot.stopme()