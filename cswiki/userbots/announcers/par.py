# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

PAGE_PREFIX = "Wikipedie:Patroláři a revertéři/Žádosti"
PAGE_LIST = "Wikipedie:Patroláři a revertéři/Žádosti"
RE_SECTION = re.compile(r'^==[^=\n]+(|.*[^=\n]+)==\s*$', re.MULTILINE)
RE_SUBPAGE = re.compile(r'\{\{[^\}\n]*/(?P<subpage>[^\}\n]+)\}\}')
RE_CLOSE = re.compile(r"\* '''Lhůta pro vyjádření:''' ([0-9]+\. [0-9]+\.) [0-9]+")


def get_candidates(site):
	page = pywikibot.Page(site, PAGE_LIST)
	last_section = re.split(RE_SECTION, page.get())[-1]
	out = []
	for candidate in RE_SUBPAGE.finditer(last_section):
		subpage_name = candidate.group('subpage')
		subpage = pywikibot.Page(site, u'%s/%s' % (PAGE_PREFIX, subpage_name))
		if subpage.exists():
			close = RE_CLOSE.search(subpage.text)
			out.append({
				'PREFIX': PAGE_PREFIX,
				'subpage_name': subpage_name,
				'close': close.group(1),
			})
	return out


ANNOUNCES = [
		{'page': u'Šablona:OznámeníRC/PAR', 'big_tl': u'|- id="Sablona--OznameniRC__Oznameni_PAR"\n! [[Wikipedie:Patroláři a revertéři|Patrolář/revertér]]:\n| %s<noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>\n', 'small_tl': u"[[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (do %(close)s)", 'separator': u' • ', 'empty': u'<!-- momentálně tu nic není --><noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>'},
		{'page': u'Wikipedie:Portál Wikipedie/Co se děje/Žádosti o PAR', 'big_tl': u'%s\n', 'small_tl': u"* [[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (do %(close)s)", 'separator': u'\n', 'empty': u'<!-- momentálně tu nic není -->'},
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
			comment = u'hlásič PAR hlásá (počet: %s)' % len(candidates)
			page.put(new_text, comment=comment)


if __name__ == '__main__':
	site = pywikibot.Site()
	candidates = get_candidates(site)
	announce_candidates(site, candidates)
	pywikibot.stopme()
