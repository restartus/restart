name ?= $$(basename $(PWD))
MAIN ?= $(name).py
WEB ?= $(MAIN)
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py" -not -name $(WEB))
FLAGS ?=

## main: run the main program
.PHONY: main
main:
	pipenv run python $(MAIN) $(FLAGS)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	pipenv run python -m pdb $(MAIN) $(FLAGS)

## streamlit: use streamlit to run the graphical interface (deprecated)
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: streamlit
streamlit:
	pipenv run streamlit run $(WEB) -- $(FLAGS)

## web-debug: run web interface in debugger (deprecated)
streamlit-debug:
	pipenv run python -m pdb $(WEB) $(FLAGS)
