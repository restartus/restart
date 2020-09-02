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
