#
## Model user commands:
# Python Makefile template (install python 3.8 and test tools)
# Configure by setting PIP for pip packages and optionally name
# requires include.mk
#
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
# If you need the infra/bin tools, then you need to set the build to run
# relatively there
MAIN ?= $$(basename $(PWD)).py
# main.py includes streamlit code that only runs when streamlit invoked
WEB ?= $(MAIN)
LIB ?= lib
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py"  -not -name $(WEB))
FLAGS ?=
flags ?= -p 8501:8501
PIP ?= streamlit altair pandas pyyaml xlrd tables
# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916
PIP_DEV ?=

DOC ?= doc


.DEFAULT_GOAL := help

## main: run the main program
.PHONY: main
main:
	pipenv run python $(MAIN) $(FLAGS)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	pipenv run python -m pdb $(MAIN)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	pipenv run python -d $(MAIN) $(FLAGS)

## web: use streamlit to run the graphical interface
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: web
web:
	pipenv run streamlit run $(WEB) -- $(FLAGS)

## web-pdb: single step debug
web-pdb:
	pipenv run pdb $(WEB) $(FLAGS)
## web-debug: run web interface in debugger
web-debug:
	pipenv run python -m pdb $(WEB) $(FLAGS)

#
# https://pipenv.pypa.io/en/latest/install/
# https://realpython.com/pipenv-guide/
# install everything including things just needed for edevelopment
##
## update: installs all pipenv packages
.PHONY: update
update:
	pipenv update

## install: Install with pipenv as virtual environment (runs pipenv-clean first)
# Note that black is still prelease so need --pre
# pipenv clean removes all packages not in the virtual environment
.PHONY: install
PYTHON = 3.8
install: pipenv-python
	[[ -n $(PIP_DEV) ]] && pipenv install --dev $(PIP_DEV) || true
	[[ -n $(PIP) ]] && pipenv install $(PIP) || true
	pipenv lock

# https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e
# https://medium.com/@peterkong/comparison-of-python-documentation-generators-660203ca3804
## doc: make the documentation for the Python project (uses pipenv)
.PHONY: doc
doc:
	for file in $(all_py); do pipenv run pdoc --force --html --output $(DOC) $$file; done

.PHONY: doc-web
doc-web:
	for file in $(all_web); do pipenv run pdoc --force --html --output $(DOC) $$file; done

## doc-debug: run web server to look at docs (uses pipenv)
.PHONY: doc-debug
doc-debug:
	@echo browse to http://localhost:8080 and CTRL-C when done
	for file in $(all_py); do pipenv run pdoc --http : $(DOC) $$file; done

.PHONY: doc-debug-web
doc-debug-web:
	@echo browse to http://localhost:8080 and CTRL-C when done
	pipenv run pdoc --http : $(WEB)

## format: reformat python code to standards
# exclude web black does not grok streamlit but not conformas
# pipenv run black -l 79 $(NO_WEB)
.PHONY: format
format:
	# the default is 88 but pyflakes wants 79
	pipenv run isort --profile=black -w 79 .
	pipenv run black -l 79 *.py

## pypi: push the package to the Python library (uses pipenv)
.PHONY: pypi
pypi:
	pipenv run python setup.py register -r pypi
	pipenv run python setup.py sdit upload -r pypi

##
## gcloud: push up to Google Cloud
.PHONY: gcloud
gcloud:
	gcloud projects list
