export LC_ALL=en_US.UTF-8
export PYTHONIOENCODING=utf8
cd /data/project/urbanecmbot/11bots/cswiki/userbots/addPrekladCT
sql cswiki < sql.sql | sed 1d > preklads.txt
cp -r preklads.txt ~/tmpPublic/
python generateExceptions.py > exceptions.txt
cut -f 1 < preklads.txt | sort -u | grep -F -x -v -f exceptions.txt > pages.txt
python3 addmissing.py -always -intersect -file:pages.txt -search:'-insource:/\{\{[Pp]řeklad/'
rm *.txt
cd $OLDPWD
