name ?= $$(basename $(PWD))
MAIN ?= $(name).py
WEB ?= $(MAIN)
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py" -not -name $(WEB))
FLAGS ?=
CA_FLAGS ?=
WA_FLAGS ?=

## main: run the main program
.PHONY: main
main:
	pipenv run python $(MAIN) $(FLAGS)

## main-ca: run the california model
.PHONY: main-ca
main-ca:
	pipenv run python $(MAIN) $(CA_FLAGS)

.PHONY: main-wa
main-wa:
	pipenv run python $(MAIN) $(WA_FLAGS)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	pipenv run python -m pdb $(MAIN) $(FLAGS)

## pdb-ca: run debugging on california model
.PHONY: pdb-ca
pdb-ca:
	pipenv run python -m pdb $(MAIN) $(CA-FLAGS)

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

.PHONY:
web-ca:
	pipenv run streamlit run $(WEB) -- $(CA_FLAGS)

.PHONY:
web-wa:
	pipenv run streamlit run $(WEB) -- $(WA_FLAGS)
