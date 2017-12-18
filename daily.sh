export LC_ALL=en_US.UTF-8
/data/project/urbanecmbot/11bots/standardization.sh
python /data/project/urbanecmbot/exportWikidataModule/export.py &>> /data/project/urbanecmbot/logs/exportWD.log
bash /data/project/urbanecmbot/addPrekladCT/run.sh
bash /data/project/urbanecmbot/wikidataCoorImport/run.sh
python /data/project/urbanecmbot/relikty/deletethem.py
python /data/project/urbanecmbot/orphan/to_delete_orphan.py
/data/project/urbanecmbot/11bots/badprotecttemplates.sh
python /data/project/urbanecmbot/ukoly/addPriority.py
python /data/project/urbanecmbot/ukoly/bezPodstranky.py
python /data/project/urbanecmbot/mostLinkedDisambigs/mostLinkedDisambigs.py
cd /data/project/urbanecmbot/autoprotect
python daily.py
cd $OLDPWD
