#!/usr/bin/env python

import requests
import pywikibot
from lxml import html
import toolforge

requests.utils.default_user_agent = lambda: "Dashboard Scrapper (no website exists, martin.urbanec@wikimedia.cz, https://meta.wikimedia.org/wiki/User:Martin_Urbanec)"

site = pywikibot.Site()

campaigns = [
    'seniori',
    'wikimedia_čr__senioři_všichni',
]

users = []
for campaign in campaigns:
    r = requests.get("https://outreachdashboard.wmflabs.org/campaigns/%s/users" % campaign)
    tree = html.fromstring(r.content)
    users_ = tree.xpath('//*[@id="users"]/table/tbody/tr/td/a/text()')
    for user in users_:
        if user.encode('latin1').decode('utf8') not in ('Gampe', 'Vojtěch Veselý', 'Frettie', 'Gabriela Boková (WMCZ)', 'Ikcur', 'Czeva'):
            users.append('"' + user.encode('latin1').decode('utf8') + '"')


conn = toolforge.connect('cswiki')
with conn.cursor() as cur:
    cur.execute('''SELECT page_title
        FROM revision_userindex
        JOIN page ON page_id=rev_page
        JOIN actor ON actor_id=rev_actor
        WHERE actor_name IN (%s)
        AND rev_parent_id=0
        AND page_namespace=0
        AND page_is_redirect=0
        AND rev_timestamp > CURRENT_TIMESTAMP - INTERVAL 3 MONTH
        ORDER BY rev_timestamp DESC''' % ", ".join(users))
    data = cur.fetchall()

page = pywikibot.Page(site, "Wikipedie:Údržbové seznamy/Nové články založené seniory/seznam")
page.text = ""
for row in data:
    page.text += "* [[%s]]\n" % row[0].decode('utf-8')
page.save('Robot: Aktualizace seznamu')
