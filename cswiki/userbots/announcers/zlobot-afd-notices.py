# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

AFD_PREFIX = u'Wikipedie:Diskuse o smazání'
AFD_LIST = u'Wikipedie:Diskuse o smazání/seznam'
RE_SECTION = re.compile(r'^==[^=\n]+(|.*[^=\n]+)==\s*$', re.MULTILINE)
RE_SUBPAGE = re.compile(r'\{\{[^\}\n]+/(?P<subpage>[^\}\n]+)\}\}')
#RE_LINK = re.compile(r'\[\[(?P<link>[^\]\n\|]+)(\|[^\]\n]+)?\]\]')
RE_SINCE = re.compile(r'^;\s*Diskus.{0,2}otev.{0,20}:\s*\n:.*\s+(?P<date>\d{1,2}\.\s*\d{1,2}\.\s\d{2,4}, \d{1,2}:\d{2} \([^\)]+\))', re.MULTILINE)
RE_CLOSE = re.compile(r'^;\s*Uzav.{1,3}en.{1,3} diskuse:\s*\n:\s*(?:(?P<default>standardn.{1,3}: t.{1,3}den po zah.{1,3}jen.{1,3}))|(?:.*<!--\s*(?P<custom>.*\S)\s*-->)', re.MULTILINE)

def get_afd_candidates(site):
	afd = pywikibot.Page(site, AFD_LIST)
	last_section = re.split(RE_SECTION, afd.get())[-1]
	out = []
	for candidate in RE_SUBPAGE.finditer(last_section):
		subpage_name = candidate.group('subpage')
		subpage = pywikibot.Page(site, u'%s/%s' % (AFD_PREFIX, subpage_name))
		since = RE_SINCE.search(subpage.get())
		close = RE_CLOSE.search(subpage.get())
		
		if close == None or (close.group('default') == None and close.group('custom') == None):
			# fail
			close_text = u'konec?'
		elif close.group('custom') != None:
			# custom close
			close_text = close.group('custom')
		elif since == None:
			close_text = u'začátek?'
		else:
			# default close: one week
			open_ts = datetime.datetime.strptime(since.group('date'), '%d. %m. %Y, %H:%M (%Z)')
			close_ts = open_ts + datetime.timedelta(7)
			if close_ts < datetime.datetime.now():
				close_text = u'zralé'
			else:
				close_text = u'do&nbsp;%d.&nbsp;%d.' % (close_ts.day, close_ts.month)
		
		out.append({
			'AFD': AFD_PREFIX,
			'subpage_name': subpage_name,
			'close': close_text,
		})
	return out

ANNOUNCES = [
	{'page':u'User:Zlobot/AfD-OznámeníRC', 'big_tl':u'|- id="Sablona--OznameniRC__Oznameni_Hlasovani_o_smazani"\n! [[Wikipedie:Diskuse o smazání|Diskuse o&nbsp;smazání]]:\n| %s\n', 'small_tl':u"[[%(AFD)s/%(subpage_name)s|%(subpage_name)s]] (%(close)s)", 'separator':u' • ', 'empty':u'<!-- momentálně tu nic není -->'},
	{'page':u'User:Zlobot/AfD-PortálWP', 'big_tl':u'%s\n', 'small_tl':u"* [[%(AFD)s/%(subpage_name)s|%(subpage_name)s]] (%(close)s)", 'separator':u'\n', 'empty':u'<!-- momentálně tu nic není -->'},
]

def announce_afd_candidates(site, candidates):
	for announce in ANNOUNCES:
		if len(candidates) > 0:
			items = [announce['small_tl'] % candidate for candidate in candidates]
			inner_text = announce['separator'].join(items)
			new_text = announce['big_tl'] % inner_text
		else:
			new_text = announce['empty']
		page = pywikibot.Page(site, announce['page'])
		if new_text.strip() != page.get().strip():
			comment = u'hlásič AfD hlásá (počet: %s)' % len(candidates)
			page.put(new_text, comment=comment)
		

if __name__ == '__main__':
	site = pywikibot.Site()
	candidates = get_afd_candidates(site)
	announce_afd_candidates(site, candidates)
	pywikibot.stopme()
