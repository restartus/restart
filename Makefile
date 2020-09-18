#
# Makefile for the project supports Docker running as gitpod locally
# Or in gitpod land
#
TAG ?= v3.0


flags ?= -e GRANT_SUDO=1
Dockerfile := Dockerfile
DOCKER_USER ?= jovyan
DOCKER_UID ?= $(DOCKER_USER)

Dockerfile.in := $(Dockerfile).in
dest_dir ?= /home/$(DOCKER_USER)/workspace
volumes ?= -v $$(readlink -f "."):$(dest_dir)/restart \
		   -v $$(readlink -f "../data"):$(dest_dir)/data
#		   -v $$(readlink -f "config"):$(dest_dir)/restart/config \
#		   -v $$(readlink -f "lib"):$(dest_dir)/restart/lib \

# Model targets
MAIN ?= restart.main
MOD ?= restart.module_test
FLAGS ?= --config restart
CA_FLAGS ?= --config restart --pop oes --state California --subpop healthcare
CA_VENT_FLAGS ?= --config config/ca-vent
WA_FLAGS ?= --config restart --pop oes --state Washington

# the packages and config needed for the main package and notebooks
PIPENV_CHECK_FLAGS ?= -i 38212
# The order matters because of PYTHON so put it first
include lib/include.src.mk
include nb/include.nb.mk

## Dockerfile fix because .gitpod does not proecss correctly
## Note this is Mac only
$(Dockerfile): $(Dockerfile.in) lib/lib.docker lib/debug.docker lib/restart.docker

## gitpod: Make dockerfile for gitpod
# we need to do envsubst since gitpod.io does not honor ARGS
.PHONY: gitpod
gitpod:
	m4 <.gitpod.Dockerfile.in | \
	DOCKER_USER=gitpod \
	DOCKER_UID="33333"  \
	PYTHON="$(PYTHON)" \
	PIP="$(PIP)" \
	PIP_ONLY="$(PIP_ONLY)" \
	PIP_DEV="$(PIP_DEV)" \
		envsubst '$$DOCKER_USER \
			      $$DOCKER_UID \
				  $$PYTHON \
				  $$PIP \
				  $$PIP_ONLY \
				  $$PIP_DEV' \
			> .gitpod.Dockerfile


## tmux: open up set windows to debug in python setup with tmuxinator
.PHONY: tmux
tmux:
	tmuxinator

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
	$(RUN) python -m pdb -m $(MAIN) $(FLAGS)

## debug: run with debug model on for main
.PHONY: debug
debug:
	$(RUN) python -d -m $(MAIN) $(FLAGS)

## ca-main: run California model
.PHONY: ca-main
ca-main:
	$(RUN) python -m $(MAIN) $(CA_FLAGS)

## ca-pdb: debug CA model
.PHONY: ca-pdb
ca-pdb:
	$(RUN) python -m pdb -m $(MAIN) $(CA_FLAGS)

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
	$(RUN) python -m pdb -m $(MAIN) $(CA_VENT_FLAGS)

# wa-main run WA model
.PHONY: wa-main
wa-main:
	$(RUN) python -m $(MAIN) $(WA_FLAGS)

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	$(RUN) python -m $(MAIN) --pop oes --state Indiana --county "St. Joseph" --output config/sj/config.yaml
	$(RUN) python -m $(MAIN)--pop wa --output config/wa/config.yaml

include lib/include.mk
include lib/include.python.mk
include lib/include.docker.mk
