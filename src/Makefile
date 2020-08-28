#
# Makefile tuned for Python and Streamlit
#
# overriding the name
TAG ?= v2.2
name ?= model
MAIN ?= main.py
FLAGS = --pop dict
CA_FLAGS ?= --config ../config/ca-oes --pop oes --state California --subpop healthcare
CA_VENT_FLAGS = --config ../config/ca-vent

# Note that main run

## main-ca: run the california model using oes data
.PHONY: ca-main
ca-main:
	pipenv run python $(MAIN) $(CA_FLAGS)

## ca-vent: Ventilator analysis for California
.PHONY: ca-vent
ca-vent:
	pipenv run python $(MAIN) $(CA_VENT_FLAGS)

## ca-vent-pdb: Debug California ventilator analysis
.PHONE: ca-vent-pdb
ca-vent-pdb:
	pipenv run python -m pdb $(MAIN) $(CA_VENT_FLAGS)

## wa-main run washington model
.PHONY: wa-main
wa-main:
	pipenv run python $(MAIN) $(WA_FLAGS)

## ca-pdb: run debugging on california model
.PHONY: ca-pdb
ca-pdb:
	pipenv run python -m pdb $(MAIN) $(CA_FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	pipenv run python -d $(MAIN) $(FLAGS)

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	pipenv run python main.py --pop oes --state Indiana --county "St. Joseph" --output ../config/sj/config.yaml
	pipenv run python main.py --pop wa --output ../config/wa/config.yaml

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
