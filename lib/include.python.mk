## Model user commands:
# Python Makefile template (install python 3.8 and test tools)CTI
# Configure by setting PIP for pip packages and optionally name
# requires include.mk
#
# Remember makefile *must* use tabs instead of spaces so use this vim line
#
# The makefiles are self documenting, you use two leading
# for make help to produce output
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use to add comments when running make help
#
FLAGS ?=
SHELL ?= /bin/bash
all_py = $$(find . -name "*.py")
all_yaml = $$(find . -name "*.yaml")
# gitpod needs three digits
PYTHON ?= 3.8.5
DOC ?= doc
LIB ?= lib
name ?= $$(basename $(PWD))
MAIN ?= $(name).py
STREAMLIT ?= $(MAIN)
# As of September 2020, run jupyter 0.2 and this generates a pipenv error
# so ignore it
PIPENV_CHECK_FLAGS ?= --ignore 38212

# https://stackoverflow.com/questions/589276/how-can-i-use-bash-syntax-in-makefile-targets
# The virtual environment [ pipenv | conda | none ]
ENV ?= pipenv
RUN ?=
ACTIVATE ?=
UPDATE ?=
INSTALL ?=
DEV_INSTALL ?= $(INSTALL)
ifeq ($(ENV),pipenv)
	RUN := pipenv run
	ACTIVATE :=
	UPDATE := pipenv update
	INSTALL := pipenv install
	INSTALL_DEV := $(INSTALL) --dev --pre
else ifeq ($(ENV),conda)
	RUN := conda run -n $(name)
	ACTIVATE := eval "$$(conda shell.bash hook)" &&
	UPDATE := $(RUN) conda update --all
	INSTALL := conda install -y -n $(name)
	INSTALL_DEV := $(INSTALL)
else ifeq ($(ENV),none)
	RUN :=
	ACTIVATE :=
	# need a noop as this is not a modifier
	# https://stackoverflow.com/questions/12404661/what-is-the-use-case-of-noop-in-bash
	UPDATE := :
	INSTALL :=
	INSTALL_DEV := $(INSTALL)
endif


# test-env: Test environment
.PHONY: test-env
test-env:
	@echo 'ENV="$(ENV)" RUN="$(RUN)"'
# The calling Makefile should set these should be at least one

PIP ?=
PIP_DEV ?=
# These cannot be installed in the environment must use pip install
PIP_ONLY ?=

# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916
#
## test-type: Test the types NB, SRC and STREAMLIT
.PHONY: test-type
test-type:
	@echo 'SRC="$(SRC)" NB="$(NB)" STREAMLIT="$(STREAMLIT)"'

## update: installs all pipenv packages
.PHONY: update
update:
	$(UPDATE)

## install: install packages
# Note that black is still prelease so need --pre
.PHONY: install
install:
ifeq ($(ENV),conda)
		conda env list | grep ^$(name) || conda create -y --name $(name)
		$(ACTIVATE) conda activate $(name)
		conda config --env --add channels conda-forge
		conda config --env --set channel_priority strict
		conda install --name $(name) -y python=$(PYTHON)
endif
	$(INSTALL) $(PIP) || true
	$(INSTALL_DEV) $(PIP_DEV) || true
	$(RUN) pip install $(PIP_ONLY) || true

ifeq ($(ENV),pipenv)
		pipenv lock
		pipenv update
endif
	@echo this does not work on WSL so you need to run pre-commit install manually
	[[ -e .pre-commit-config.yaml ]] && $(RUN) pre-commit install || true


# https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e
# https://medium.com/@peterkong/comparison-of-python-documentation-generators-660203ca3804
## doc: make the documentation for the Python project (uses pipenv)
.PHONY: doc
doc:
	for file in $(all_py); \
		do $(RUN) pdoc --force --html --output $(DOC) $$file; \
	done

## doc-debug: run web server to look at docs (uses pipenv)
.PHONY: doc-debug
doc-debug:
	@echo browse to http://localhost:8080 and CTRL-C when done
	for file in $(all_py); \
		do pipenv run pdoc --http : $(DOC) $$file; \
	done

## format: reformat python code to standards
.PHONY: format
format:
	# the default is 88 but pyflakes wants 79
	$(RUN) isort --profile=black -w 79 .
	$(RUN) black -l 79 *.py

## pipenv-package: build package
.PHONY: package
package:
	$(RUN) python setup.py sdist bdist_wheel

## pypi: build package and push to the python package index
.PHONY: pypi
pypi: package
	$(RUN) twine upload dist/*

## pypi-test: build package and push to test python package index
.PHONY: pypi-test
pypi-test: package
	$(RUN) twine upload --repository-url https://test.pypi.org/legacy/ dist/*

## pipenv: Run interactive commands in Pipenv environment
.PHONY: pipenv
pipenv:
	pipenv shell

## pipenv-lock: Install from the lock file (for deployment and test)
.PHONY: pipenv-lock
pipenv-lock:
	pipenv install --ignore-pipfile

# https://stackoverflow.com/questions/53382383/makefile-cant-use-conda-activate
# https://github.com/conda/conda/issues/7980
## conda-clean: Remove conda and start all over
.PHONY: conda-clean
conda-clean:
	$(ACTIVATE) && conda activate base
	conda env remove -n $(name) || true
	conda clean -afy

## conda: activate conda environment
.PHONY: conda
conda:
	$(ACTIVATE) && conda activate $(name)

## lint : code check (conda)
.PHONY: lint
lint:
	$(RUN) flake8 || true
ifdef all_py
	$(RUN) seed-isort-config ||true
	$(RUN) mypy --namespace-packages $(all_py) || true
	$(RUN) bandit $(all_py) || true
	$(RUN) pydocstyle --convention=google $(all_py) || true
endif
ifdef all_yaml
	$(RUN) yamllint $(all_yaml) || true
endif

# Flake8 does not handle streamlit correctly so exclude it
# Nor does pydocstyle
# If the web can pass then you can use these lines
# pipenv run flake8 --exclude $(STREAMLIT)
#	pipenv run mypy $(NO_STREAMLIT)
#	pipenv run pydocstyle --convention=google --match='(?!$(STREAMLIT))'
#
## pipenv-lint: cleans code for you
.PHONY: pipenv-lint
pipenv-lint: lint
	pipenv check $(PIPENV_CHECK_FLAGS)

## pre-commit: Run pre-commit hooks
.PHONY: pre-commit
pre-commit:
	[[ -e .pre-commit-config.yaml ]] && $(RUN) pre-commit autoupdate || true
	[[ -e .pre-commit-config.yaml ]] && $(RUN) pre-commit run --all-files || true
##
## Installation helpers (users should not need to invoke):

## pipenv-python: Install python version in
# also add to the python path
# This fail if we don't have brew
# Note when you delete the Pipfile, it will search recursively upward
# looking for one, so on clean recreate one
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
# Then add a dummy pipenv so that you do not move up recursively
# And create an environment in the current directory
.PHONY: pipenv-clean
pipenv-clean:
	pipenv --rm || true
	rm Pipfile* || true
	touch Pipfile
