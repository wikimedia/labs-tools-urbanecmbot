#!/bin/bash

/data/project/urbanecmbot/11bots/wikidatawiki/coorImport/basic.sh 'http://petscan.wmflabs.org/?language=cs&project=wikipedia&depth=10&categories=%C3%9Adr%C5%BEba%3ABez%20sou%C5%99adnic%20na%20Wikidatech&ns%5B0%5D=1&templates_any=Infobox%20-%20budova%0D%0AInfobox%20-%20kostel%0D%0AInfobox%20-%20s%C3%ADdlo%0D%0AInfobox%20-%20s%C3%ADdlo%20sv%C4%9Bta%0D%0AInfobox%20-%20vodn%C3%AD%20tok&interface_language=en&&doit=&format=tsv'
/data/project/urbanecmbot/11bots/wikidatawiki/coorImport/basic.sh 'http://petscan.wmflabs.org/?language=sk&project=wikipedia&ns%5B0%5D=1&templates_any=Infobox%20Kostol%0D%0AInfobox%20s%C3%ADdlo&interface_language=en&&doit=&format=tsv' '-lang:sk'
