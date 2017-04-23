python ~/pwb/scripts/replace.py -always -ns:0 -summary:'Robot: Odebrání odrážky před šablonou překlad' -search:'insource:/\* ?\{\{[Pp]řeklad/' -regex '\* ?\{\{[Pp]řeklad' '{{Překlad'
python ~/pwb/scripts/replace.py -always -ns:0 -search:'insource:/===* *Zdroj *===*.\{\{[Pp]řeklad/' -summary:'Robot: Standardizace' '== Zdroj ==' '== Reference =='
python ~/pwb/scripts/replace.py -always -ns:0 -search:'insource:/===* *Zdroje *===*.\{\{[Pp]řeklad/' -summary:'Robot: Standardizace' '== Zdroje ==' '== Reference =='
python ~/pwb/scripts/replace.py -always -ns:0 -summary:'Robot: Standardizace' -search:'insource:/===* *Externí zdroje *===*/' '== Externí zdroje ==' '== Externí odkazy =='
python ~/pwb/scripts/replace.py -summary:'Robot: {{reflist}} => <references />' -always -ns:0 -regex -search:'insource:/\{\{[Rf]eflist\|?[^}]*\}\}/' '\{\{[Rf]eflist\|?[^}]*\}\}' '<references />'
