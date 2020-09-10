#
# Makefile for the project supports Docker running as gitpod locally
# Or in gitpod land
#
TAG ?= v2.5

Dockerfile := Dockerfile
Dockerfile.in := $(Dockerfile).in
DOCKER_USER := joyvan
flags ?= -e GRANT_SUDO=1
DOCKER_USER ?= jovyan
# Using same layout as gitpod
dest_dir ?= /home/$(DOCKER_USER)/workspace
volumes ?= -v $$(readlink -f "."):$(dest_dir)/restart/restart \
		   -v $$(readlink -f "../config"):$(dest_dir)/restart/config \
		   -v $$(readlink -f "../lib"):$(dest_dir)/restart/lib \
		   -v $$(readlink -f "../../data"):$(dest_dir)/data

Gitpod := .gitpod.Dockerfile
Gitpod.in := $(Gitpod).in
GITPOD_USER := gitpod
GITPOD_NAME := $(GITPOD_USER)

# Model targets
MAIN ?= restart.main
MOD ?= restart.module_test
FLAGS ?= --config restart
CA_FLAGS_OLD ?= --config restart --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config config/ca-vent
WA_FLAGS ?= --config restart --pop oes --state Washington

# the packages and config needed for the main package and notebooks
PIPENV_CHECK_FLAGS ?= -i 38212
include lib/include.src.mk
include nb/include.nb.mk

$(Dockerfile): $(Dockerfile.in) lib/lib.docker lib/debug.docker restart.docker

## gitpod: Make dockerfile for gitpod
.PHONY: gitpod
gitpod: $(Gitpod)

## repo-pre-commit: Install the base precommit for the repo
.PHONY: repo-pre-commit
repo-pre-commit:
	[[ -e .pre-commit-config.yaml ]] || ln -s lib/root.pre-commit-config.yaml .pre-commit-config.yaml

## pypi-clean: Fix the pypi cache
.PHONY: pypi-clean
pypi-clean:
	rm -r build dist *.egg-info/

## test: run system test
.PHONY: test
test: main ca-main ca-vent wa-main module-test

## main: run the main program
.PHONY: main
main:
	$(RUN) python -m $(MAIN) $(FLAGS)

## pdb: run locally with python to test components from main
.PHONY: pdb
pdb:
	$(RUN) python -m pdb $(MAIN) $(FLAGS)

## ca-main: run California model
.PHONY: ca-main
ca-main:
	$(RUN) python -m $(MAIN) $(CA_FLAGS)

## ca-pdb: debug CA model
.PHONY: ca-pdb
ca-pdb:
	$(RUN) python -m pdb $(MAIN) $(CA_FLAGS)

## ca-vent: vent analysis for California
.PHONY: ca-vent
ca-vent:
	$(RUN) python -m $(MAIN) $(CA_VENT_FLAGS)

## module-test: test python import of model
.PHONY: module-test
module-test:
	$(RUN) python -m $(MOD)

## ca-vent-pdb: debug CA vent analysis
.PHONY: ca-vent-pdb
ca-vent-pdb:
	$(RUN) python -m pdb $(MAIN) $(CA_VENT_FLAGS)

# wa-main run WA model
.PHONY: wa-main
wa-main:
	$(RUN) python -m $(MAIN) $(WA_FLAGS)

## pipenv-streamlit: use streamlit to run the graphical interface (deprecated)
# bug as of July 2020 cannot send flags to python
# https://discuss.streamlit.io/t/command-line-arguments/386
.PHONY: streamlit
streamlit:
	$(RUN) streamlit run -m $(WEB) -- $(FLAGS)

## pipenv-streamlit-debug: run web interface in debugger (deprecated)
.PHONY: streamlit-debug
streamlit-debug:
	$(RUN) python -m pdb $(WEB) $(FLAGS)

## debug: run with debugging outputs on
.PHONY: debug
debug:
	$(RUN) python -d -m $(MAIN) $(FLAGS)

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	$(RUN) python -m $(MAIN) --pop oes --state Indiana --county "St. Joseph" --output config/sj/config.yaml
	$(RUN) python -m $(MAIN)--pop wa --output config/wa/config.yaml

.PHONY: streamlit-ca
## streamlit-ca: Run streamlit with California flags (deprecated)
streamlit-ca:
	$(RUN) streamlit run -m $(WEB) -- $(CA_FLAGS)

.PHONY: streamlit-wa
## streamlit-wa: Run streamlit with Washington flags (deprecated)
streamlit-wa:
	$(RUN) streamlit run -m $(WEB) -- $(WA_FLAGS)

include lib/include.mk
include lib/include.python.mk
include lib/include.docker.mk
