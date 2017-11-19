# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import pywikibot
import re

from datetime import date, timedelta
from time import strftime, strptime

from pywikibot import textlib
from pywikibot.pagegenerators import PrefixingPageGenerator
from pywikibot.tools import OrderedDict

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

months = {
    1: 'ledna',
    2: 'února',
    3: 'března',
    4: 'dubna',
    5: 'května',
    6: 'června',
    7: 'července',
    8: 'srpna',
    9: 'září',
    10: 'října',
    11: 'listopadu',
    12: 'prosince',
}

def find_templates(text):
    '''From textlib.extract_templates_and_params_regex_simple'''
    result = []

    for match in textlib.NESTED_TEMPLATE_REGEX.finditer(text):
        name, params = match.group(1), match.group(2)
        if name.strip().lower() != 'zajímavost':
            continue

        if params is None:
            params = []
        else:
            params = params.split('|')

        numbered_param_identifiers = iter(range(1, len(params) + 1))

        params = OrderedDict(
            arg.split('=', 1)
            if '=' in arg
            else (str(next(numbered_param_identifiers)), arg)
            for arg in params)

        result.append((match.span(), params))

    return result


def localized(date, upto=None):
    ret = str(date.day) + '.'
    if upto != 'month':
        ret += ' ' + str(months[date.month])
        if upto != 'year':
            ret += ' ' + str(date.year)
    return ret


def get_date(split):
    _, year, week = split
    my_time = strptime(year, '%Y')  # 1. ledna
    week_delta = int(week) - int(strftime('%W', my_time))  # o kolik týdnů
    monday = date(int(year), 1, 1) + timedelta(days=week_delta * 7)
    monday -= timedelta(days=my_time.tm_wday)  # skok na pondělí
    sunday = monday + timedelta(days=6)  # ... a neděli
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
    text = text.replace("'" * 3, '')
    text = text.replace("'" * 2, '')
    return text.lower().strip()


def my_get(data, my_key):
    for key in data:
        if key.strip() == my_key.strip():
            return data[key]
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
        if (my_get(params, 'do')
                and plain_text(until) == plain_text(my_get(params, 'do'))):
            return span, params
    return None


def handle_page(page):
    split = page.title().split('/')
    if len(split) != 3:
        return
    link = '/'.join(split)
    for match in lineR.finditer(page.text):
        text = match.group(1)
        titleM = titleR.search(text)
        if not titleM:
            continue
        talkpage = pywikibot.Page(site, titleM.group(1)).toggleTalkPage()
        text = titleR.sub(lambda m: m.group(2) or m.group(1), text, count=1).lstrip('.…')
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
            for key in mapping.keys():
                val = my_get(params, key)
                if val:
                    data[mapping[key]] = val.strip()
            change = False
            if not set(['since', 'until']) <= set(data.keys()):
                since, until = get_date(split)
                data.update({
                    'since': since,
                    'until': until,
                })
                change = True
            if 'link' not in data:
                data['link'] = link
                change = True
            if not change:
                continue
            start, end = span
            new_text = (talkpage.text[:start] + pattern % data
                        + talkpage.text[end:])
            summary = 'doplnění [[%s|zajímavosti]]' % link
        else:
            since, until = get_date(split)
            data = {'text': text, 'link': link, 'since': since, 'until': until}
            template = pattern % data
            new_text = template + '\n' + talkpage.text.lstrip()
            summary = 'uvedení [[%s|zajímavosti]]' % link
        pywikibot.showDiff(talkpage.text, new_text)
        talkpage.put(new_text, summary=summary, apply_cosmetic_changes=False)


def run(gen):
    for page in gen:
        handle_page(page)


if '-current' in args:
    suffix = strftime('%Y/%W')
    pywikibot.output('Doing week: %s' % suffix)
    handle_page(pywikibot.Page(site, 'Wikipedie:Zajímavosti/%s' % suffix))
else:
    gen = PrefixingPageGenerator(
        'Wikipedie:Zajímavosti/201', includeredirects=False, site=site, content=True)
    run(gen)
