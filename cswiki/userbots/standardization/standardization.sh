#!/bin/bash

python3 ~/pwb/scripts/replace.py -always -ns:0 -summary:'Robot: Odebrání odrážky před šablonou překlad' -search:'insource:/\* ?\{\{[Pp]řeklad/' -regex '\* ?\{\{[Pp]řeklad' '{{Překlad'
python3 ~/pwb/scripts/replace.py -always -ns:0 -search:'insource:/===* *Zdroj *===*.\{\{[Pp]řeklad/' -summary:'Robot: Standardizace' '== Zdroj ==' '== Reference =='
python3 ~/pwb/scripts/replace.py -always -ns:0 -search:'insource:/===* *Zdroje *===*.\{\{[Pp]řeklad/' -summary:'Robot: Standardizace' '== Zdroje ==' '== Reference =='
#python3 ~/pwb/scripts/replace.py -always -ns:0 -summary:'Robot: Standardizace' -search:'insource:/===* *Externí zdroje *===*/' '== Externí zdroje ==' '== Externí odkazy =='
python3 ~/pwb/scripts/replace.py -always -summary:"Robot: Standardizace" -ns:0 -search:'insource:/===? ?Viz (též|také) ?===?/' -regex '(===? ?)Viz (též|také)( ?===?)' '\1Související články\3'
python3 ~/pwb/scripts/replace.py -always -summary:"Robot: Standardizace" -ns:0 -search:'insource:/===? ?Dále také ?===?/' -regex '(===? ?)Dále také( ?===?)' '\1Související články\2'
python3 ~/pwb/scripts/replace.py -always -ns:0 -summary:"Robot: Standardizace" -search:'insource:/== ?Odkazy ?==..references ?../' -regex '(== ?)Odkazy( ?==)\n<references ?/>' '\1Reference\2\n<references />'

# custom standardizations
source ~/toolforge/bin/activate
python3 ~/11bots/cswiki/userbots/standardization/replace-reflist.py
