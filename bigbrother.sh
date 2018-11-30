#!/bin/bash

# Jobs started with `-continuous` should be re-started automatically by the Grid Engine.
# Unfortunatelly, some out-of-memory situations can mean the wrapper script that is
# responsible for re-starting the job is also killed.
#
# This script is a fallback method to re-start jobs in case the Grid Engine wasn't
# able to re-start them itself. This script needed because the tool that did this
# job was deprecated (https://wikitech.wikimedia.org/wiki/Help:Toolforge/Grid#Bigbrother)

if [ $# -ne 2 ]; then
  echo "Usage: $0 <jobname> <command>"
  exit 1
fi

JOBNAME="$1"
COMMAND="$2"

function log {
  echo "$(date -Iseconds) $1"
}

function restart_needed {
  if ! /usr/bin/qstat | cut -d' ' -f3 | grep "${JOBNAME:0:10}" >/dev/null 2>&1; then
    return 0
  else
    return 1
  fi
}

function submit_job {
  /usr/bin/jstart -N "$JOBNAME" "$COMMAND"
}

if restart_needed; then
  log "Restarting job '$JOBNAME' ('$COMMAND')"
  submit_job
fi
