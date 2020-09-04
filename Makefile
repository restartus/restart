#
# Makefile for Gitpod and other project-wise use
#
#
## Make sure to run make .gitpod.Dockerfile  before commits
Dockerfile := .gitpod.Dockerfile
Dockerfile.in := $(Dockerfile).in

$(Dockerfile): $(Dockerfile.in) lib/lib.docker nb/nb.docker src/src.docker

# gitpod: Test the gitpod Dockerfile
.PHONY: gitpod
gitpod: $(Dockerfile)
	docker build -f $(Dockerfile) lib

include lib/include.docker.mk
include lib/include.mk
include lib/include.python.mk
