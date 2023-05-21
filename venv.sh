#!/bin/bash

cd ~

git clone --recursive --branch stable "https://gerrit.wikimedia.org/r/pywikibot/core" $HOME/pywikibot-core

python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip setuptools wheel
pip install $HOME/pywikibot-core[mwoauth,mysql,requests,requests_oauthlib]  # update as needed
