#
#
##
## Base user commands:
# Configure by setting PIP for pip packages and optionally name
#
# Remember makefile *must* use tabs instead of spaces so use this vim line
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading
# for make help to produce output
#
# These should be overridden in the makefile that includes this, but this sets # defaults use to add comments when running make help
#
# Two entry points in MAIN and WEB
# https://stackoverflow.com/questions/589276/how-can-i-use-bash-syntax-in-makefile-targets
SHELL :- /bin/bash
repo ?= restartus
name ?= $$(basename "$(PWD)")
user ?= $$USER
all_py = $$(find . -name "*.py")
all_yaml = $$(find . -name "*.yaml")

# These are the base packages that we always use
# includes above this are for specific purposes like airflow
BASE_PIP ?=
BASE_PIP_DEV ?= --pre nptyping pydocstyle pdoc3 flake8 mypy bandit \
								 black tox pytest pytest-cov pytest-xdist tox yamllint \
								 pre-commit isort seed-isort-config

.DEFAULT_GOAL := help

.PHONY: help
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file
## help: available commands (the default)
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)

## shell: Run interactive commands in Pipenv environment
.PHONY: shell
shell:
	pipenv shell

# Flake8 does not handle streamlit correctly so exclude it
# Nor does pydocstyle
# If the web can pass then you can use these lines
# pipenv run flake8 --exclude $(WEB)
#	pipenv run mypy $(NO_WEB)
#	pipenv run pydocstyle --convention=google --match='(?!$(WEB))'
#
## lint: cleans code for you
.PHONY: lint
lint:
	pipenv check
	# ensures isortworks correctly
	# mypy finds more errors than flake and we are using namespace
	# https://mypy.readthedocs.io/en/latest/running_mypy.html#missing-imports
	# note this has a bug if there are no yaml or python files
	# the brackets test if they exist at all
	# We set the last to true so we don't get an error code if trhere
	# are no such files
	# Note that with precommit installed, theres are pretty redundant, but keep
	# here unitl it's verfiedjj
	pipenv run flake8
ifdef all_py
	pipenv run seed-isort-config || true
	pipenv run mypy --namespace-packages $(all_py) || true
	pipenv run bandit $(all_py) || true
	pipenv run pydocstyle --convention=google $(all_py) || true
endif
	# lint the yaml config files and kill the error if it doesn't exist
ifdef all_yaml
	pipenv run yamllint $(all_yaml) || true
endif
	@echo if you want destructive formatting run make format
	[[ -e .pre-commit-config.yaml ]] && pipenv run pre-commit autoupdate || true
	[[ -e .pre-commit-config.yaml ]] && pipenv run pre-commit run --all-files || true

##
## Installation helpers (users should not need to invoke):
## base-pipenv: Install with pipenv as virtual environment (defaults to 3.8 and clean)
# Note that black is still prelease so need --pre
# pipenv clean removes all packages not in the virtual environment
.PHONY: base-pipenv
base-pipenv: pipenv-python
	echo $$SHELL
ifdef BASE_PIP_DEV
	pipenv install --dev $(BASE_PIP_DEV) || true
endif
ifdef PIP_DEV
  pipenv install $(BASE_PIP) || true
endif
	pipenv update
	[[ -e .pre-commit-config.yaml ]] && pipenv run pre-commit install || true

## pipenv-python: Install python version in $(PYTHON)
# also add to the python path
# This faile if we don't have brew
PYTHON ?= 3.8
.PHONY: pipenv-python
pipenv-python: pipenv-clean
	@echo currently using python $(PYTHON) override changing PYTHON make flag
	brew upgrade python@$(PYTHON) pipenv
	@echo pipenv sometimes corrupts after python $(PYTHON) install so reinstall if needed
	pipenv --version || brew reinstall pipenv
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --python /usr/local/opt/python@$(PYTHON)/bin/python3
	pipenv clean
	@echo use .env to ensure we can see all packages
	grep ^PYTHONPATH .env ||  echo "PYTHONPATH=." >> .env

## pipenv-clean: cleans the pipenv completely
# note pipenv --rm will fail if there is nothing there so ignore that
# do not do a pipenv clean until later otherwise it creats an environment
# Same with the remove if the files are not there
.PHONY: pipenv-clean
pipenv-clean:
	pipenv --rm || true
	rm Pipfile* || true
