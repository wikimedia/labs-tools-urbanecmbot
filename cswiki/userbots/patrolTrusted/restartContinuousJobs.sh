#!/bin/bash

# Maintenance script to restart continuous jobs - for some unknown reasons, they can't run forever.
# Let's restart them once per day and see if that helps.

qdel patrolTrusted > /dev/null
qdel patrolSandbox > /dev/null
qdel patrolAfterPatrol > /dev/null
sleep 20
jstart -quiet -N patrolTrusted /data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/patrolTrusted.sh
jstart -quiet -N  patrolAfterPatrol /data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/patrolEditsAfterArticle.sh
jstart -quiet  -N patrolSandbox /data/project/urbanecmbot/11bots/cswiki/userbots/patrolTrusted/patrolSandbox.sh
