name ?= $$(basename $(PWD))
MAIN ?= $(name).py
WEB ?= $(MAIN)
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py" -not -name $(WEB))
FLAGS ?=
CA_FLAGS ?=
WA_FLAGS ?=
VOILA ?= $(name).ipynb

## main: run the main program
.PHONY: main
main:
	pipenv run python $(MAIN) $(FLAGS)

## main-ca: run the california model
.PHONY: main-ca
main-ca:
	pipenv run python $(MAIN) $(CA_FLAGS)

## main-wa: run washington model
.PHONY: main-wa
main-wa:
	pipenv run python $(MAIN) $(WA_FLAGS)

## pdb-org: run pdb with model and organization demand
pdb-org:
	pipenv run python -m pdb $(MAIN) --organization dict

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	pipenv run python -m pdb $(MAIN) $(FLAGS)

## pdb-ca: run debugging on california model
.PHONY: pdb-ca
pdb-ca:
	pipenv run python -m pdb $(MAIN) $(CA_FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	pipenv run python -d $(MAIN) $(FLAGS)

## streamlit: use streamlit to run the graphical interface (deprecated)
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: streamlit
streamlit:
	pipenv run streamlit run $(WEB) -- $(FLAGS)

## web-debug: run web interface in debugger (deprecated)
streamlit-debug:
	pipenv run python -m pdb $(WEB) $(FLAGS)

.PHONY: streamlit-ca
## streamlit-ca: Run streamlit with California flags (deprecated)
streamlit-ca:
	pipenv run streamlit run $(WEB) -- $(CA_FLAGS)

.PHONY: streamlit-wa
## streamlit-wa: Run streamlit with Washington flags (deprecated)
streamlit-wa:
	pipenv run streamlit run $(WEB) -- $(WA_FLAGS)

.PHONY: voila
## voila: Start Jupyter to interactive Dashboard in current directory
voila:
	pipenv run voila $(VOILA)
