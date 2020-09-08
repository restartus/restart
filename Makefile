#
# Makefile for Gitpod and other project-wise use
#
#
## Make sure to run make .gitpod.Dockerfile  before commits
Dockerfile := .gitpod.Dockerfile
Dockerfile.in := $(Dockerfile).in
DOCKER_USER := gitpod
name := gitpod


$(Dockerfile): $(Dockerfile.in) lib/lib.docker nb/nb.docker restart/restart.docker lib/debug.docker

## gitpod: Make dockerfile for gitpod
.PHONY: gitpod
gitpod: $(Dockerfile)

## repo-pre-commit: Install the base precommit for the repo
.PHONY: repo-pre-commit
repo-pre-commit:
	[[ -e .pre-commit-config.yaml ]] || ln -s lib/root.pre-commit-config.yaml .pre-commit-config.yaml

include lib/include.docker.mk
include lib/include.mk

## pypi-clean: Fix the pypi cache
.PHONY: pypi-clean
pypi-clean:
	rm -r build dist *.egg-info/
