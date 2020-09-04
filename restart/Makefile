#
# Make for a python package
#
# simple only runs in gnu
TAG ?= v2.5
MAIN ?= main.py

FLAGS ?= --pop dict
CA_FLAGS ?= --config ../config/ca-oes --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config ../config/ca-vent
# voila requires jupyter-server 0.1.1
# PIPENV_CHECK_FLAGS ?= -i 38212
# For docker config link in key directories
flags ?= -e GRANT_SUDO=1
DOCKER_USER ?= jovyan
dest_dir ?= /home/$(DOCKER_USER)/ws
volumes ?= -v $$(readlink -f "../src"):$(dest_dir)/restart/src \
		   -v $$(readlink -f "../config"):$(dest_dir)/restart/config \
		   -v $$(readlink -f "../lib"):$(dest_dir)/restart/lib \
		   -v $$(readlink -f "../../data"):$(dest_dir)/data

PIP += pandas confuse ipysheet pyomo h5py
		   # pyyaml xlrd
PIP_ONLY += tables
# These are for development time
PIP_DEV += nptyping pydocstyle pdoc3 flake8 mypy bandit \
  		   black tox pytest pytest-cov pytest-xdist tox yamllint \
		   pre-commit isort seed-isort-config \
		   setuptools wheel twine

Dockerfile = Dockerfile
Dockerfile.in = $(Dockerfile).in
$(Dockerfile): $(Dockerfile.in) ../lib/debug.docker ../lib/lib.docker src.docker

# Note that main run
## test: run system test
.PHONY: test
test: main ca-main ca-vent wa-main

## main: run the main program
.PHONY: main
main:
	$(RUN) python $(MAIN) $(FLAGS)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (uses pipenv)
.PHONY: pdb
pdb:
	$(RUN) python -m pdb $(MAIN) $(FLAGS)

## pipenv-streamlit: use streamlit to run the graphical interface (deprecated)
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: streamlit
streamlit:
	$(RUN) streamlit run $(WEB) -- $(FLAGS)

## pipenv-streamlit-debug: run web interface in debugger (deprecated)
.PHONY: streamlit-debug
streamlit-debug:
	$(RUN) python -m pdb $(WEB) $(FLAGS)
## ca-main: run California model
.PHONY: ca-main
ca-main:
	$(RUN) python $(MAIN) $(CA_FLAGS)

## ca-vent: Ventilator analysis for California
.PHONY: ca-vent
ca-vent:
	$(RUN) python $(MAIN) $(CA_VENT_FLAGS)

## ca-vent-pdb: Debug California ventilator analysis
.PHONE: ca-vent-pdb
ca-vent-pdb:
	$(RUN) python -m pdb $(MAIN) $(CA_VENT_FLAGS)

## wa-main run washington model
.PHONY: wa-main
wa-main:
	$(RUN) python $(MAIN) $(WA_FLAGS)

## ca-pdb: run debugging on california model
.PHONY: ca-pdb
ca-pdb:
	$(RUN) python -m pdb $(MAIN) $(CA_FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	$(RUN) python -d $(MAIN) $(FLAGS)

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	$(RUN) python main.py --pop oes --state Indiana --county "St. Joseph" --output ../config/sj/config.yaml
	$(RUN) python main.py --pop wa --output ../config/wa/config.yaml

.PHONY: streamlit-ca
## streamlit-ca: Run streamlit with California flags (deprecated)
streamlit-ca:
	$(RUN) streamlit run $(WEB) -- $(CA_FLAGS)

.PHONY: streamlit-wa
## streamlit-wa: Run streamlit with Washington flags (deprecated)
streamlit-wa:
	$(RUN) streamlit run $(WEB) -- $(WA_FLAGS)

include ../lib/include.mk
include ../lib/include.python.mk
include ../lib/include.docker.mk
