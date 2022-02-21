# -*- coding: utf-8 -*-
from datetime import datetime, timedelta

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

PAGE_PREFIX = "Wikipedie:Nominace nejlepších článků"
PAGE_LIST = "Wikipedie:Nominace nejlepších článků"
RE_SUBPAGE = re.compile(r'\{\{[^\}\n]*/(?P<subpage>[^\}\n]+)\}\}')
RE_VOTING = re.compile(r'==== ?Hlasování ?====\s*\n.*(?!==)')
RE_SIGNATURE = re.compile(r'\[\[(Wikipedista|Wikipedistka):[^|]+\|[^]]+\]\]( \(|, )\[\[Diskuse s (wikipedistou|wikipedistkou):[^|]+\|[dD]iskuse\]\]\)?[^\d]*([0-9]+)\. ([0-9]+)\. ([0-9]{4}), ([0-9]+):([0-9]+) \((CET|CEST)')
RE_UNUSUAL_CLOSE = re.compile(r'==== ?Hlasování ?====\s*\n<!--([^-]+)-->')


def get_candidates(site):
	page = pywikibot.Page(site, PAGE_LIST)
	out = {
		"voting": [],
		"discussion": []
	}
	for candidate in RE_SUBPAGE.finditer(page.text):
		subpage_name = candidate.group('subpage')
		subpage = pywikibot.Page(site, u'%s/%s' % (PAGE_PREFIX, subpage_name))
		if not subpage.exists():
			continue # workaround, {{/Velký modrák}} and similar guiding things in the page
		print('Processing %s' % subpage.title())
		voting = RE_VOTING.search(subpage.text)
		if voting is None:
			first_signature = RE_SIGNATURE.search(subpage.text)
			out["discussion"].append({
				"PREFIX": PAGE_PREFIX,
				"subpage_name": subpage_name,
				"date": "od %s. %s." % (first_signature.group(4), first_signature.group(5))
			})
		else:
			unusual_close = RE_UNUSUAL_CLOSE.search(subpage.text)
			if unusual_close is None or unusual_close.group(1).strip() == "standardní":
				voting_start_m = RE_SIGNATURE.search(voting.group(0))
				voting_start = datetime(int(voting_start_m.group(6)), int(voting_start_m.group(5)), int(voting_start_m.group(4)))
				voting_end = voting_start + timedelta(days=14) # votings usually lasts 14 days
				voting_end = voting_end.strftime('%-d. %-m.')
			else:
				voting_end = unusual_close.group(1).strip()
			out["voting"].append({
				'PREFIX': PAGE_PREFIX,
				'subpage_name': subpage_name,
				'date': "do %s" % voting_end
			})
	return out


ANNOUNCES = [
		{'page': u'Šablona:OznámeníRC/NNČ', 'big_separator': "", 'big_big_big_tl': '|- id="Sablona--OznameniRC__Oznameni_Nejlepsi-clanky"\n![[Wikipedie:Nominace nejlepších článků|Nejlepší články]]:\n| %s<noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>\n', 'big_big_tl': "<div>'''%(description)s''': %(data)s</div>", 'big_tl': "%s", 'small_tl': u"[[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (%(date)s)", 'separator': u' • ', 'empty': '<!-- momentálně tu nic není --><noinclude>\n[[Kategorie:Šablony:Části šablon]]\n[[Kategorie:Šablony:MediaWiki]]\n</noinclude>', 'inner_empty': u'<div></div>'},
		{'page': u'Wikipedie:Portál Wikipedie/Co se děje/Nominace nejlepších článků', 'big_separator': '\n', 'big_big_big_tl': '%s', 'big_big_tl': "'''%(description)s''': %(data)s", 'big_tl': u'\n%s\n', 'small_tl': u"* [[%(PREFIX)s/%(subpage_name)s|%(subpage_name)s]] (%(date)s)", 'separator': u'\n', 'empty': '<!-- momentálně tu nic není -->', 'inner_empty': u'<div></div>'},
]

DESCRIPTIONS = {
	'discussion': 'Diskuse',
	'voting': 'Hlasování'
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
			page.save('hlásič NNČ hlásá')


if __name__ == '__main__':
	site = pywikibot.Site()
	candidates = get_candidates(site)
	announce_candidates(site, [
		{'type': 'discussion', 'data': candidates['discussion']},
		{'type': 'voting', 'data': candidates['voting']}
	])
	pywikibot.stopme()
