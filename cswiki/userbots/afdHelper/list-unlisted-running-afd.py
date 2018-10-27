# -*- coding: utf-8 -*-
import datetime

import pywikibot
import time
import sys
import re

import logging
logger = logging.getLogger("pywiki")
logger.setLevel(logging.WARNING)

AFD = u'Wikipedie:Diskuse o smazání'
RE_SECTION = re.compile(r'^==[^=\n]+(|.*[^=\n]+)==\s*$', re.MULTILINE)
RE_SUBPAGE = re.compile(r'\{\{/(?P<subpage>[^\}\n]+)\}\}')
#RE_LINK = re.compile(r'\[\[(?P<link>[^\]\n\|]+)(\|[^\]\n]+)?\]\]')
RE_SINCE = re.compile(r'^;\s*Diskus.{0,2}otev.{0,20}:\s*\n:.*\s+(?P<date>\d{1,2}\.\s*\d{1,2}\.\s\d{2,4}, \d{1,2}:\d{2} \([^\)]+\))', re.MULTILINE)
RE_CLOSE = re.compile(r'^;\s*Uzav.{1,3}en.{1,3} diskuse:\s*\n:\s*(?:(?P<default>standardn.{1,3}: t.{1,3}den po zah.{1,3}jen.{1,3}))|(?:.*<!--\s*(?P<custom>.*\S)\s*-->)', re.MULTILINE)

def get_listed_afd(site):
    afd = pywikibot.Page(site, AFD)
    last_section = re.split(RE_SECTION, afd.get())[-1]
    out = []
    for candidate in RE_SUBPAGE.finditer(last_section):
        out.append(candidate.group('subpage'))
    return out

def get_unclosed_afd(site):
    out = []
    for subpage in site.allpages(namespace=4, prefix="Diskuse o smazání/"):
        if subpage.isRedirectPage():
            continue
        close = RE_CLOSE.search(subpage.get())
        if close is None:
            continue
        if close.group('custom') != u"uzavřeno":
            out.append(subpage.title())
    return out

if __name__ == '__main__':
    site = pywikibot.Site()
    listed = get_listed_afd(site)
    unclosed = get_unclosed_afd(site)
    for afd in unclosed:
        if afd not in listed:
            print(afd)