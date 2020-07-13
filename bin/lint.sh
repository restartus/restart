#!/bin/bash
set -u && SCRIPTNAME="$(basename "${BASH_SOURCE[0]}")"
SCRIPT_DIR=${SCRIPT_DIR:=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)}
RUN_DIR=$(cd $SCRIPT_DIR/../model/src && pwd)
ALL_PY=$(find $RUN_DIR -name "*.py")
ALL_YAML=$(find $RUN_DIR -name "*.yaml")

# use flake8
pip install flake8
(cd $RUN_DIR && flake8)

# use mypy
pip install mypy
(cd $RUN_DIR && mypy --namespace-packages $ALL_PY)

# use bandit
pip install bandit
(cd $RUN_DIR && bandit $ALL_PY)

# use pydocstyle
pip install pydocstyle
(cd $RUN_DIR && pydocstyle --convention=google $ALL_PY)

# use yaml linter
pip install yamllint
(cd $RUN_DIR && yamllint $ALL_YAML)

