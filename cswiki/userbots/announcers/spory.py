# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)


class ZOO:
	PAGE_PREFIX = "Wikipedie:Žádost o opatření"
	PAGE_LIST = "Wikipedie:Žádost o opatření"
	RE_SECTION = re.compile(r'=== Projednávané žádosti ===\n[^=]*')
	RE_SUBPAGE = re.compile(r'\[\[(Wikipedie:Žádost o opatření/|/[^/]*)([^/|]*)/?(|)?[^]/]+\]\]')


class ZOA:
	PAGE_PREFIX = "Wikipedie:Žádost o arbitráž"
	PAGE_LIST = "Wikipedie:Žádost o arbitráž"
	RE_SECTION = re.compile(r'== Aktuální žádosti ==\n[^=]*')
	RE_SUBPAGE = re.compile(r'\* ?\[\[/([^/]*)/\]\]')


def get_candidates(site, conf):
	page_list = pywikibot.Page(site, conf.PAGE_LIST)
	section = conf.RE_SECTION.search(page_list.text).group(0)
	candidates = conf.RE_SUBPAGE.findall(section)
	out = []
	for candidate in candidates:
		out.append({
			'PREFIX': conf.PAGE_PREFIX,
			'subpage_name': candidate[1]
		})
	return out


ANNOUNCES = [
		{'page': u'Šablona:OznámeníRC/Spory', 'big_separator': "", 'big_big_big_tl': '|- id="Sablona--Sablona--OznameniRC__Oznameni_Reseni-sporu"\n! [[Wikipedie:Řešení sporů|Řešení sporů]]:\n| %s<noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>\n', 'big_big_tl': "<div>'''%(description)s''': %(data)s</div>", 'big_tl': "%s", 'small_tl': u"[[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]]", 'separator': u' • ', 'empty': '<!-- momentálně tu nic není --><noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>', 'inner_empty': u'<div></div>'},
		{'page': u'Wikipedie:Portál Wikipedie/Co se děje/Arbitráže', 'big_separator': '\n', 'big_big_big_tl': '%s', 'big_big_tl': "'''%(description)s''': %(data)s", 'big_tl': u'\n%s\n', 'small_tl': u"* [[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]]", 'separator': u'\n', 'empty': '<!-- momentálně tu nic není -->', 'inner_empty': u'<div></div>'},
]

DESCRIPTIONS = {
	'zoos': 'Opatření',
	'zoas': 'Arbitráže'
}


def announce_candidates(site, candidates_sets):
	for announce in ANNOUNCES:
		params = []
		all_empty = True
		for candidates_set in candidates_sets:
			candidates = candidates_set['data']
			if len(candidates) > 0:
				items = [announce['small_tl'] % candidate for candidate in candidates]
				inner_text = announce['separator'].join(items)
				params.append(announce['big_big_tl'] % {
					'description': DESCRIPTIONS[candidates_set['type']],
					'data': announce['big_tl'] % inner_text
				})
				all_empty = False
			else:
				params.append(announce['inner_empty'])
		if not all_empty:
			new_text = announce['big_big_big_tl'] % announce["big_separator"].join(params)
		else:
			new_text = announce["empty"]
		page = pywikibot.Page(site, announce['page'])
		if not page.exists() or new_text.strip() != page.get().strip():
			page.text = new_text
			page.save('hlásič sporů hlásá')


if __name__ == '__main__':
	site = pywikibot.Site()
	print(get_candidates(site, ZOO))
	announce_candidates(site, [
		{'type': 'zoas', 'data': get_candidates(site, ZOA)},
		{'type': 'zoos', 'data': get_candidates(site, ZOO)}
	])
	pywikibot.stopme()
