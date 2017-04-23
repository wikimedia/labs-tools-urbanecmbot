#!/bin/bash
export PYTHONPATH=/shared/pywikipedia/core:/shared/pywikipedia/core/externals/httplib2:/shared/pywikipedia/core/scripts
python ~/pwb/scripts/clean_sandbox.py -family:wikipedia -lang:cs -hours:12
