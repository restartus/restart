#
# Makefile tuned for Python and Streamlit
#
# overriding the name
TAG ?= v2.2
name=model
FLAGS = --pop dict
CA_FLAGS = --config ../config/ca-v2.2 --pop oes --state California --subpop healthcare
MAIN = main.py

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	pipenv run python main.py --pop oes --state Indiana --county "St. Joseph" --output ../config/sj/config.yaml
	pipenv run python main.py --pop wa --output ../config/wa/config.yaml

## main-ca: run the california model
.PHONY: main-ca
main-ca:
	pipenv run python $(MAIN) $(CA_FLAGS)

## main-wa: run washington model
.PHONY: main-wa
main-wa:
	pipenv run python $(MAIN) $(WA_FLAGS)

## pdb-ca: run debugging on california model
.PHONY: pdb-ca
pdb-ca:
	pipenv run python -m pdb $(MAIN) $(CA_FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	pipenv run python -d $(MAIN) $(FLAGS)

.PHONY: streamlit-ca
## streamlit-ca: Run streamlit with California flags (deprecated)
streamlit-ca:
	pipenv run streamlit run $(WEB) -- $(CA_FLAGS)

.PHONY: streamlit-wa
## streamlit-wa: Run streamlit with Washington flags (deprecated)
streamlit-wa:
	pipenv run streamlit run $(WEB) -- $(WA_FLAGS)

include ../lib/include.mk
include ../lib/include.python.mk
include ../lib/include.model.mk
include ../lib/include.docker.mk
