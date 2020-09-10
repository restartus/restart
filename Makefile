#
# Makefile for Gitpod and other project-wise use
#
#
## Make sure to run make .gitpod.Dockerfile  before commits
Dockerfile := .gitpod.Dockerfile
Dockerfile.in := $(Dockerfile).in
DOCKER_USER := gitpod
name := gitpod

# Model targets
MAIN ?= src.main
FLAGS ?= --config src
CA_FLAGS ?= --config src --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config config/ca-vent
WA_FLAGS ?= --config config/src --pop oes --state Washington

$(Dockerfile): $(Dockerfile.in) lib/lib.docker nb/nb.docker restart/restart.docker lib/debug.docker

## gitpod: Make dockerfile for gitpod
.PHONY: gitpod
gitpod: $(Dockerfile)

## repo-pre-commit: Install the base precommit for the repo
.PHONY: repo-pre-commit
repo-pre-commit:
	[[ -e .pre-commit-config.yaml ]] || ln -s lib/root.pre-commit-config.yaml .pre-commit-config.yaml

include lib/include.mk
include lib/include.python.mk
include lib/include.docker.mk

## pypi-clean: Fix the pypi cache
.PHONY: pypi-clean
pypi-clean:
	rm -r build dist *.egg-info/

## test: run system test
.PHONY: test
test: main ca-main ca-vent wa-main

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

## ca-vent-pdb: debug CA vent analysis
.PHONY: ca-vent-pdb
ca-vent-pdb:
	$(RUN) python -m pdb $(MAIN) $(CA_VENT_FLAGS)

# wa-main run WA model
.PHONY: wa-main
wa-main:
	$(RUN) python -m $(MAIN) $(WA_FLAGS)
