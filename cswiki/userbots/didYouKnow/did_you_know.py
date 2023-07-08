# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pywikibot
import re

from datetime import date, timedelta

from pywikibot import textlib
from pywikibot.pagegenerators import GeneratorFactory, PrefixingPageGenerator
from collections import OrderedDict

args = pywikibot.handle_args()

site = pywikibot.Site('cs', 'wikipedia')

lineR = re.compile(r'^\* *(.*)', re.M)
titleR = re.compile(r"'''\[\[([^]|[]+)(?:\|([^]|[]+))?\]\]'''")

pattern = '''{{Zajímavost
 | zajímavost = %(text)s
 | link = %(link)s
 | od = %(since)s
 | do = %(until)s
}}'''

months = (
    '',
    'ledna',
    'února',
    'března',
    'dubna',
    'května',
    'června',
    'července',
    'srpna',
    'září',
    'října',
    'listopadu',
    'prosince',
)


def find_templates(text):
    '''From textlib.extract_templates_and_params_regex_simple'''
    result = []

    for match in textlib.NESTED_TEMPLATE_REGEX.finditer(text):
        name, params = match.group(1), match.group(2)
        if name and name.strip().lower() != 'zajímavost':
            continue

        if params is None:
            params = []
        else:
            params = params.split('|')
            i = 0
            while i < len(params)-1:
                if params[i].count('[') != params[i].count(']'):
                    params[i] += '|' + params.pop(i+1)
                else:
                    i += 1

        numbered_param_identifiers = iter(range(1, len(params) + 1))

        params = OrderedDict(
            arg.split('=', 1)
            if '=' in arg
            else (str(next(numbered_param_identifiers)), arg)
            for arg in params)

        result.append((match.span(), params))

    return result


def localized(date, omit=None):
    '''Localize given date, possibly omit some parts of it.'''
    ret = str(date.day) + '.'
    if omit != 'month':
        ret += ' ' + str(months[date.month])
        if omit != 'year':
            ret += ' ' + str(date.year)
    return ret


def get_date(split):
    '''Get localized date span for given ISO week.'''
    _, year, week = split
    # ISO week 01 is the one with 4th January
    fourth_Jan = date(int(year), 1, 4)
    week_delta = int(week) - 1
    monday = fourth_Jan + timedelta(days=week_delta * 7)
    if monday.weekday():
        monday -= timedelta(days=monday.weekday())  # adjust to Monday
    sunday = monday + timedelta(days=6)  # ... then compute Sunday
    if monday.year != sunday.year:
        return localized(monday), localized(sunday)
    elif monday.month != sunday.month:
        return localized(monday, 'year'), localized(sunday)
    else:
        return localized(monday, 'month'), localized(sunday)


def plain_text(text):
    text = text.replace('&nbsp;', ' ')
    while ' ' * 2 in text:
        text = text.replace(' ' * 2, ' ')
    text = re.sub(r'\[\[([^]|]+\|)?([^]|[]+)\]\]', r'\2', text)
    text = text.replace("'" * 3, '')
    text = text.replace("'" * 2, '')
    return text.lower().strip()


def my_get(data, my_key):
    for key, value in data.items():
        if key.strip() == my_key.strip():
            return value
    return None


def find_same(old_text, my_text, split):
    my_plain = plain_text(my_text)
    since, until = get_date(split)
    for span, params in find_templates(old_text):
        if my_get(params, 'link') and plain_text(my_get(params, 'link')) == plain_text('/'.join(split)):
            return span, params
        if (my_get(params, 'zajímavost')
                and my_plain == plain_text(my_get(params, 'zajímavost'))):
            return span, params
        if (my_get(params, 'od')
                and plain_text(since) == plain_text(my_get(params, 'od'))):
            return span, params
        if (my_get(params, 'do')
                and plain_text(until) == plain_text(my_get(params, 'do'))):
            return span, params
    return None


def handle_page(page, force=False):
    link = page.title()
    split = link.split('/')
    if len(split) != 3:
        return
    for match in lineR.finditer(page.text):
        text = match.group(1)
        titleM = titleR.search(text)
        if not titleM:
            continue
        article = pywikibot.Page(site, titleM.group(1))
        if not article.exists() or article.isRedirectPage():
            continue
        talkpage = article.toggleTalkPage()
        if talkpage.site != site:
            continue
        text = titleR.sub(lambda m: m.group(2) or m.group(1), text, count=1)
        text = text.lstrip('.…')
        text = text.replace(" ''(na obrázku)''", '')
        text = text.replace(" (''na obrázku'')", '')
        text = text.replace(' (na obrázku)', '')
        same = find_same(talkpage.text, text, split)
        if same:
            mapping = {
                'zajímavost': 'text',
                'link': 'link',
                'od': 'since',
                'do': 'until',
            }
            span, params = same
            data = {}
            for key in mapping:
                val = my_get(params, key)
                if val:
                    data[mapping[key]] = val.strip()
            change = False
            if force or ('since' not in data or 'until' not in data):
                since, until = get_date(split)
                data.update({
                    'since': since,
                    'until': until,
                })
                change = True
            if force or 'link' not in data:
                data['link'] = link
                change = True
            if not change:
                continue
            start, end = span
            new = pattern % data
            old_sort = my_get(params, 'sort')
            if old_sort:
                new = (new[:-3]  # 3 chars: newline and two end braces
                       + ' | sort = %s\n}}' % old_sort.strip())
            new_text = talkpage.text[:start] + new + talkpage.text[end:]
            summary = 'doplnění [[%s|zajímavosti]]' % link
        else:
            since, until = get_date(split)
            data = {'text': text, 'link': link, 'since': since, 'until': until}
            template = pattern % data
            new_text = template + '\n' + talkpage.text.lstrip()
            summary = 'uvedení [[%s|zajímavosti]]' % link
        pywikibot.showDiff(talkpage.text, new_text)
        talkpage.put(new_text, summary=summary, minor=False, apply_cosmetic_changes=False)


def run(gen, force=False):
    for page in gen:
        handle_page(page, force=force)


if __name__ == '__main__':
    if '-current' in args:
        # ISO week is the one with 4th January
        # workaround needed for < 3.6
        # XXX: what happens before 4th January?
        day = date.today()
        if day.replace(month=1, day=4).strftime('%W') == '00':
            day += timedelta(days=7)
        suffix = day.strftime('%Y/%W')
        pywikibot.output('Doing week: ' + suffix)
        handle_page(pywikibot.Page(site, 'Wikipedie:Zajímavosti/' + suffix),
                    force='-force' in args)
    else:
        genFactory = GeneratorFactory(site=site)
        for arg in args:
            genFactory.handleArg(arg)
        gen = genFactory.getCombinedGenerator(preload=True)
        if not gen:
            gen = PrefixingPageGenerator(
                'Wikipedie:Zajímavosti/20', includeredirects=False, site=site,
                content=True)
        run(gen, force='-force' in args)
