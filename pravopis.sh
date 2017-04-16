#!/bin/bash
python ~/pwb/scripts/replace.py -always -ns:0 -search:vyjímk 'vyjímk' 'výjimk' -summary:Pravopis
python ~/pwb/scripts/replace.py -always -regex -ns:0 -start:! "[Čč]esk(á|é|ou) Republi(ce|k[auy]|kou)" "Česk\1 republi\2" -summary:Pravopis
