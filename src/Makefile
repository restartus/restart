#
# Makefile tuned for Python and Streamlit
#
# overriding the name
TAG ?= v2.5
MAIN ?= main.py
FLAGS = --pop dict
CA_FLAGS ?= --config ../config/ca-oes --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config ../config/ca-vent
# voila requires jupyter-server 0.1.1
# PIPENV_CHECK_FLAGS ?= -i 38212
# For docker config link in key directories
DOCKER_USER ?= jovyan
dest_dir ?= /home/$(DOCKER_USER)/ws
volumes ?= -v $$(readlink -f "../src"):$(dest_dir)/restart/src \
		   -v $$(readlink -f "../config"):$(dest_dir)/restart/config \
		   -v $$(readlink -f "../lib"):$(dest_dir)/restart/lib \
		   -v $$(readlink -f "../../data"):$(dest_dir)/data

# turn off notebook output
NB_PIP =
# Note that main run
## test: run system test
.PHONY: test
test: pipenv-test

# note do not run lint as well causes a loop
## conda-test: test with conda
.PHONY: conda-test
conda-test: main ca-main ca-vent wa-main

## pipenv-test: run system test
# note do not run lint as well causes a loop
.PHONY: pipenv-test
pipenv-test: pipenv-ca-main pipenv-main pipenv-ca-vent pipenv-wa-main

## pipenv-main-ca: run the California model using OES data (deprecated)
.PHONY: pipenv-ca-main
pipenv-ca-main:
	pipenv run python $(MAIN) $(CA_FLAGS)

## ca-main: run California model
.PHONY: ca-main
ca-main:
	$(CONDA_RUN) python $(MAIN) $(CA_FLAGS)

## pipenv-ca-vent: Ventilator analysis for California
.PHONY: pipenv-ca-vent
pipenv-ca-vent:
	pipenv run python $(MAIN) $(CA_VENT_FLAGS)

## ca-vent: Ventilator analysis for California
.PHONY: ca-vent
ca-vent:
	$(CONDA_RUN) python $(MAIN) $(CA_VENT_FLAGS)

## ca-vent-pdb: Debug California ventilator analysis
.PHONE: ca-vent-pdb
ca-vent-pdb:
	$(CONDA_RUN) python -m pdb $(MAIN) $(CA_VENT_FLAGS)

## pipenv-ca-vent-pdb: Debug California ventilator analysis
.PHONE: pipenv-ca-vent-pdb
pipenv-ca-vent-pdb:
	pipenv run python -m pdb $(MAIN) $(CA_VENT_FLAGS)

## wa-main run washington model
.PHONY: wa-main
wa-main:
	$(CONDA_RUN) python $(MAIN) $(WA_FLAGS)

## pipenv-wa-main run washington model
.PHONY: pipenv-wa-main
pipenv-wa-main:
	pipenv run python $(MAIN) $(WA_FLAGS)

## ca-pdb: run debugging on california model
.PHONY: ca-pdb
ca-pdb:
	$(CONDA_RUN) python -m pdb $(MAIN) $(CA_FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	$(CONDA_RUN) python -d $(MAIN) $(FLAGS)

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	$(CONDA_RUN) python main.py --pop oes --state Indiana --county "St. Joseph" --output ../config/sj/config.yaml
	$(CONDA_RUN) python main.py --pop wa --output ../config/wa/config.yaml

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
include ../lib/include.docker.mk
