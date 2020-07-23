#
#
# BAse configuration
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
# These should be overridden in the makefile that includes this, but this sets
# defaults use to add comments when running make help
#
# Two entry points in MAIN and WEB
# https://stackoverflow.com/questions/589276/how-can-i-use-bash-syntax-in-makefile-targets
SHELL :- /bin/bash
repo ?= restartus
name ?= $$(basename "$(PWD)")

.DEFAULT_GOAL := help

.PHONY: help
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)

## pipenv-python: Install latest python 3.x for bleeding edge features
# also add to the python path
.PHONY: pipenv-python
pipenv-python:	pipenv-clean
	@echo python is currently python 3.8
	@echo note do not use requirements.txt as it will read it by default
	@echo get the latest python
	brew upgrade python@3.8 pipenv
	PIPENV_IGNORE_VIRTUALENVS=1 pipenv install --python /usr/local/opt/python@3.8/bin/python3
	pipenv clean
	 @echo use .env to ensure we can see all packages
	 #[[ ! -e .env ]] && echo "PYTHONPATH=${PWD}" > .env

## pipenv-clean: cleans the pipenv completely
# note pipenv --rm will fail if there is nothing there so ignore that
# do not do a pipenv clean until later otherwise it creats an environment
# Same with the remove if the files are not there
#
.PHONY: pipenv-clean
pipenv-clean:
	pipenv --rm || true
	rm Pipfile* || true

## pre-commit: install git pre-commit
.PHONY: pre-commit
pre-commit:
	pipenv run pre-commit install
