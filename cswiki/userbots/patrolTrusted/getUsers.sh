#!/bin/bash
curl 'https://cs.wikipedia.org/wiki/Wikipedista:UrbanecmBot/EditPatrol?action=raw' 2> /dev/null | grep -vE '</?pre>' | sed 's/ *$//g;s/^ *//g' > /data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/editpatrol.txt
