#
##
## Docker additions for make files
# Remember makefile *must* use tabs instead of spaces so use this vim line
# requires include.mk
#
# The makefiles are self documenting, you use two leading for make help to produce output
#
# Uses m4 for includes so Dockerfile.in are processed this way
# since docker does not support a macro language
# https://www3.physnet.uni-hamburg.de/physnet/Tru64-Unix/HTML/APS32DTE/M4XXXXXX.HTM
# Assumes GNU M4 is installed
# https://github.com/moby/moby/issues/735
#
name ?= "$$(basename $(PWD))"
Dockerfile ?= Dockerfile
Dockerfile.in ?= $(Dockerfile).in
image ?= $(repo)/$(name)
container := $(name)
build_path ?= .
MAIN ?= $(name).py
DOCKER_USER ?= jovyan
DOCKER_ENV ?= docker
CONDA_ENV ?= $(name)
SHELL ?= /bin/bash

# pip packages that can also be installed by conda
PIP ?=
# pip packages that cannot be conda installed
PIP_ONLY ?=

dest_dir ?= /home/$(DOCKER_USER)/$(name)
volumes ?= -v $$(readlink -f "."):$(dest_dir)
flags ?=
docker_flags ?= --build-arg "DOCKER_USER=$(DOCKER_USER)" \
				--build-arg "NB_USER=$(DOCKER_USER)" \
				--build-arg "ENV=$(DOCKER_ENV)" \
				--build-arg "PYTHON=$(PYTHON)" \
				--build-arg "PIP=$(PIP)" \
				--build-arg "PIP_ONLY=$(PIP_ONLY)" \
# main.py includes streamlit code that only runs when streamlit invoked
# --restart=unless-stopped  not needed now

## docker: pull docker image and builds locally along with tag with git sha
$(Dockerfile): $(Dockerfile.in)
	m4 <"$(Dockerfile.in)" >"$(Dockerfile)"

.PHONY: docker
docker: $(Dockerfile)
	docker build --pull \
				$(docker_flags) \
				 -f "$(Dockerfile)" \
				 -t "$(image)" \
				 $(build_path)
	docker tag $(image) $(image):$$(git rev-parse HEAD)
	docker push $(image)

## docker-build-debug
.PHONY: docker-build-debug
docker-build-debug: $(Dockerfile)
	docker build --pull \
				--no-cache $(docker_flags) \
				 -f "$(Dockerfile)" \
				 -t "$(image)" \
				 $(build_path)

## docker-lint
.PHONY: docker-lint
docker-lint: $(Dockerfile)
	dockerfilelint $(Dockerfile)

## push: after a build will push the image up
.PHONY: push
push:
	# need to push and pull to make sure the entire cluster has the right images
	docker push $(image)

# for those times when we make a change in but the Dockerfile does not notice
# In the no cache case do not pull as this will give you stale layers
## nocache: does not use docker hub prevent stale layers from being downloaded
.PHONY: no-cache
no-cache:
	docker build --no-cache --build-arg USER=$(DOCKER_USER) \
		--build-arg NB_USER=$(DOCKER_USER) -f $(Dockerfile) -t $(image) .
	docker push $(image)
	docker pull $(image)

for_containers = bash -c 'for container in $$(docker ps -a | grep "$$0" | awk "{print \$$NF}"); \
						  do \
						  	echo docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  	docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  done'

## stop: halts all running containers
.PHONY: stop
stop:
	@$(for_containers) $(container) stop
	@$(for_containers) $(container) "rm -v"

## pull: pulls the latest image
.PHONY: pull
pull:
	docker pull $(image)

## run: stops all the containers and then runs one locally
.PHONY: run
run: stop
	last=$$(docker ps | grep $(image) | awk '{print $$NF}' | cut -d/ -f2 | awk 'BEGIN { FS="-" }; {print $$NF}' | sort -r | head -n1) ; \
	echo last found is $$last ; \
	docker run -dt \
		--name $(container)-$$((last+1)) \
		$(volumes) $(flags) $(image); \
	sleep 4; \
	docker logs $(container)-$$((last+1))

## shell: run the interactive shell in the container
.PHONY: shell
shell: stop
	docker pull $(image)
	docker run -it \
		--name $(container)-$$((last+1)) \
		$(volumes) $(flags) $(image) bash

## docker-debug: interactive but do not pull for use offline
.PHONY: docker-debug
docker-debug: stop
	@docker run -it $(flags) --name $(container) $(image) bash

## resume: keep running an existing container
.PHONY: resume
resume:
	docker start -ai $(container)

# Note we say only the type file because otherwise it tries to delete $(docker_data) itself
## prune: Save some space on docker
.PHONY: prune
prune:
	docker system prune --volumes
