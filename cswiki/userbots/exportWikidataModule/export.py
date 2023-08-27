#!/usr/bin/env python
#-*- coding: utf-8 -*-

import pywikibot
import toolforge

# Connect to database
conn = toolforge.connect('cswiki')

# Get all relevant page titles from the database
cur = conn.cursor()
with cur:
    sql = 'select page_title from page where page_namespace=828 and page_title like "Wikidata/%" and page_title not like "%/testcases%" and page_title not like "%/sandbox%" and page_title!="Wikidata/";'
    cur.execute(sql)
    data = cur.fetchall()

# Create site objects
siteour = pywikibot.Site()
sites = [
    {
        "site": pywikibot.Site('cs', 'wikiversity'),
        "dependencies": [],
    },
    {
        "site": pywikibot.Site('cs', 'wikibooks'),
        "dependencies": [
            "Module:No globals",
            'Module:Functions',
            'Module:Arguments',
        ],
    },
]

# Create summary constant
summary = u'Robot: Aktualizace Wikidata modulů'


def syncPage(siteforegin, page_title):
    pageour = pywikibot.Page(siteour, page_title)
    pageforegin = pywikibot.Page(siteforegin, page_title)
    if "Dokumentace" in page_title:
            newtext = "Tato stránka je pravidelně aktualizována robotem. Jakákoliv modifikace bude při příští aktualizaci přepsána a je třeba ji provádět na Wikipedii.\n\n" + pageour.text
    else:
        newtext = '-- Tato stránka je pravidelně aktualizována robotem. Jakákoliv modifikace bude při příští aktualizaci přepsána a je třeba ji provádět na Wikipedii. \n\n' + pageour.text
    pageforegin.text = newtext
    pageforegin.save(summary)


for site in sites:
    # Export Modul:Wikidata
    siteforegin = site["site"]
    syncPage(siteforegin, "Modul:Wikidata")

    for dependency in site["dependencies"]:
        syncPage(siteforegin, dependency)

    docpageour = pywikibot.Page(siteour, 'MediaWiki:Scribunto-doc-page-name')
    docpageforegin = pywikibot.Page(siteforegin, 'MediaWiki:Scribunto-doc-page-name')
    doDoc = docpageour.text == docpageforegin.text

    # Export all other Modul:Wikidata subpages
    for row in data:
        pagetitle = 'Modul:' + row[0].decode('utf-8')
        if 'Dokumentace' in pagetitle and not doDoc:
            continue
        syncPage(siteforegin, pagetitle)
