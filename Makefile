#
# Makefile for Gitpod and other project-wise use
#
#
## Make sure to run make .gitpod.Dockerfile  before commits
Dockerfile := Dockerfile
Dockerfile.in := $(Dockerfile).in
DOCKER_USER := gitpod
name := gitpod

# Model targets
MAIN ?= restart.main
MOD ?= restart.module_test
FLAGS ?= --config restart
CA_FLAGS ?= --config restart --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config config/ca-vent
WA_FLAGS ?= --config restart --pop oes --state Washington
include restart/include.src.mk
include nb/include.nb.mk

$(Dockerfile): $(Dockerfile.in) lib/lib.docker lib/debug.docker

## gitpod: Make dockerfile for gitpod
.PHONY: gitpod
gitpod: $(Dockerfile)

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

include lib/include.mk
include lib/include.python.mk
include lib/include.docker.mk
