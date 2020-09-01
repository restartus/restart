#!/bin/bash
set -u $$ SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR=${SCRIPT_DIR:=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}

cd ${SCRIPT_DIR}/../src
if ! python main.py --pop dict
then
  if ! pipenv run main.py --pop dict; then exit 1; fi
fi
