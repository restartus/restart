## Model user commands:
# Python Makefile template (install python 3.8 and test tools)
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
CA_FLAGS ?=
all_py = $$(find . -name "*.py")
all_yaml = $$(find . -name "*.yaml")
PYTHON ?= 3.8
DOC ?= doc
LIB ?= lib
name ?= $$(basename $(PWD))
MAIN ?= $(name).py
WEB ?= $(MAIN)
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py" -not -name $(WEB))
FLAGS ?=

## main: run the main program
.PHONY: main
main:
	$(CONDA_RUN) python $(MAIN) $(FLAGS)

## pipenv-main: run the main program
.PHONY: pipenv-main
pipenv-main:
	pipenv run python $(MAIN) $(FLAGS)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	$(CONDA_RUN) python -m pdb $(MAIN) $(FLAGS)

# https://docs.python.org/3/library/pdb.html
## pipenv-pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pipenv-pdb
pipenv-pdb:
	pipenv run python -m pdb $(MAIN) $(FLAGS)

## pipenv-streamlit: use streamlit to run the graphical interface (deprecated)
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: pipenv-streamlit
pipenv-streamlit:
	pipenv run streamlit run $(WEB) -- $(FLAGS)

## pipenv-streamlit-debug: run web interface in debugger (deprecated)
.PHONY: pipenv-streamlit-debug
pipenv-streamlit-debug:
	pipenv run python -m pdb $(WEB) $(FLAGS)

# These should only be for python development
SRC_PIP ?= pandas confuse ipysheet
		   # pyyaml xlrd

SRC_PIP_ONLY ?= tables
# These are for development time
SRC_PIP_DEV ?= nptyping pydocstyle pdoc3 flake8 mypy bandit \
  		   	   black tox pytest pytest-cov pytest-xdist tox yamllint \
			   pre-commit isort seed-isort-config \
			   setuptools wheel twine

# As of August 2020, Voila will not run with a later version and each 0.x
# change is an API bump, curren version is 0.2 and this version does generate
# a pipenv check problem so we need to ignore it
# this is for notebook development
# Current bug with bqplot
NB_PIP_DEV ?= pre-commit
NB_PIP ?= voila ipywidgets ipysheet qgrid bqplot ipympl ipyvolume ipyvuetify voila-vuetify \
		  scipy confuse
NB_PIP_ONLY ?= jupyter-server

PIPENV_CHECK_FLAGS ?= --ignore 38212

# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916

.DEFAULT_GOAL := help

# https://pipenv.pypa.io/en/latest/install/
# https://realpython.com/pipenv-guide/
# install everything including things just needed for edevelopment
##
## pipenv-update: installs all pipenv packages
.PHONY: pipenv-update
pipenv-update:
	pipenv update


## conda-update: update everything
.PHONY: conda-update
conda-update:
	$(CONDA_RUN) conda update --all

## pipenv-install: Install with pipenv as virtual environment (runs pipenv-clean first)
# Note that black is still prelease so need --pre
# pipenv clean removes all packages not in the virtual environment
.PHONY: pipenv-install
pipenv-install:
ifdef SRC_PIP_DEV
	pipenv install --dev $(SRC_PIP_DEV) || true
endif
ifdef SRC_PIP
	pipenv install $(SRC_PIP) || true
endif
ifdef NB_PIP_DEV
	pipenv install --dev $(NB_PIP_DEV) || true
endif
ifdef NB_PIP
	pipenv install $(NB_PIP) $(NB_PIP_ONLY) || true
endif
	pipenv lock
	pipenv update
	[[ -e .pre-commit-config.yaml ]] && pipenv run pre-commit install || true

## conda-install: Create the conda environtment
# https://conda-forge.org/#about
.PHONY: conda-install
conda-install:
	conda env list | grep ^$(name) || conda create --name $(name)
	$(CONDA_ACTIVATE) && conda activate $(name)
	conda config --env --add channels conda-forge
	conda config --env --set channel_priority strict
ifdef SRC_PIP_DEV
	conda install --yes -n $(name) -y $(SRC_PIP_DEV) || true
endif
ifdef SRC_PIP
	conda install --yes -n $(name) $(SRC_PIP) || true
endif
ifdef NB_PIP_DEV
	conda install --yes -n $(name) $(NB_PIP_DEV) || true
endif
ifdef NB_PIP
	conda install --yes -n $(name) $(NB_PIP) || true
endif
ifdef NB_PIP_ONLY
	$(CONDA_RUN)  pip install $(NB_PIP_ONLY) || true
endif
ifdef SRC_PIP_ONLY
	$(CONDA_RUN) pip install -y $(SRC_PIP_ONLY) || true
endif


# https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e
# https://medium.com/@peterkong/comparison-of-python-documentation-generators-660203ca3804
## doc: make the documentation for the Python project (uses pipenv)
.PHONY: doc
doc:
	for file in $(all_py); do $(CONDA_RUN) pdoc --force --html --output $(DOC) $$file; done

## pipenv-doc: make the documentation for the Python project (uses pipenv)
.PHONY: pipenv-doc
pipenv-doc:
	for file in $(all_py); do pipenv run pdoc --force --html --output $(DOC) $$file; done

## pipenv-doc-debug: run web server to look at docs (uses pipenv)
.PHONY: pipenv-doc-debug
pipenv-doc-debug:
	@echo browse to http://localhost:8080 and CTRL-C when done
	for file in $(all_py); do pipenv run pdoc --http : $(DOC) $$file; done

## pipenv-doc-debug-web: For the web interface
.PHONY: pipenv-doc-debug-web
pipenv-doc-debug-web:
	@echo browse to http://localhost:8080 and CTRL-C when done
	pipenv run pdoc --http : $(WEB)

## format: reformat python code to standards
.PHONY: format
format:
	# the default is 88 but pyflakes wants 79
	$(CONDA_RUN) isort --profile=black -w 79 .
	$(CONDA_RUN) black -l 79 *.py

## pipenv-format: reformat python code to standards
# exclude web black does not grok streamlit but not conformas
# pipenv run black -l 79 $(NO_WEB)
.PHONY: pipenv-format
pipenv-format:
	# the default is 88 but pyflakes wants 79
	pipenv run isort --profile=black -w 79 .
	pipenv run black -l 79 *.py

## pipenv-package: build package
.PHONY: pipenv-package
pipenv-package:
	pipenv run python setu.py sdist bdist_wheel

## pipenv-pypi: build package and push to the python package index
.PHONY: pipenv-pypi
pipenv-pypi: package
	pipenv run twine upload dist/*

## pipenv-pypi-test: build package and push to test python package index
.PHONY: pipenv-pypi-test
pipenv-pypi-test: package
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

##
## gcloud: push up to Google Cloud
.PHONY: gcloud
gcloud:
	gcloud projects list
