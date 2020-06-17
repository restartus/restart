#
# Minimal include (does not include docker commands
#
# Remember makefile *must* use tabs instead of spaces so use this vim line
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading ## for make help to
# produce output
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use ## to add comments when running make help
## 
## Two entry points in MAIN and WEB
user ?= $$USER
MAIN ?= main.py
WEB ?= dashboard.py


.PHONY: help
.DEFAULT_GOAL := help
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need ##
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file 
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)

# https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e
## doc: make the documentation for the Python project
.PHONY: doc
doc:
	cd .. && PYTHONPATH="." pdoc --html src --output-dir docs

## requirements: Freeze Python requirements in bare machine
requirements:
	pip freeze > requirements.txt

## python: run locally with python to test components from main
.PHONY: python
python:
	python $(MAIN)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main
.PHONY: pdb
pdb:
	python -m pdb $(MAIN)

## dash: Start the dashboard with streamlit
.PHONY: dash
dash:
	streamlit run dashboard

##
##
