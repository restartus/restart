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
# main.py includes streamlit code that only runs when streamlit invoked
LIB ?= lib
FLAGS ?=
CA_FLAGS ?=
all_py = $$(find . -name "*.py")
all_yaml = $$(find . -name "*.yaml")
flags ?= -p 8501:8501
# As of july 2020, streamlit not compatible with Pandas 1.1
PIP ?= streamlit altair "pandas<1.1" pyyaml xlrd tables confuse \
			 setuptools wheel twine voila ipywidgets ipysheet qgrid bqplot
# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916
PIP_DEV ?=

DOC ?= doc


.DEFAULT_GOAL := help

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
install: base-pipenv
ifdef PIP_DEV
	pipenv install --dev $(PIP_DEV) || true
endif
ifdef PIP
	pipenv install $(PIP) || true
endif
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

## package: build package
.PHONY: package
package:
	pipenv run python setu.py sdist bdist_wheel

## pypi: build package and push to the python package index
.PHONY: pypi
pypi: package
	pipenv run twine upload dist/*

## pypi-test: build package and push to test python package index
.PHONY: pypi-test
pypi-test: package
	pipenv run twine upload --repository-url https://test.pypi.org/legacy/ dist/*

##
## gcloud: push up to Google Cloud
.PHONY: gcloud
gcloud:
	gcloud projects list
