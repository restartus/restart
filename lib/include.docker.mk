#
##
## Docker additions for make files
# Remember makefile *must* use tabs instead of spaces so use this vim line
# requires include.mk
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading
# for make help to produce output
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use to add comments when running make help
#
# Two entry points in MAIN and WEB
# https://stackoverflow.com/questions/589276/how-can-i-use-bash-syntax-in-makefile-targets

Dockerfile ?= Dockerfile
image ?= $(repo)/$(name)
container = $(name)
build_path ?= .
MAIN ?= $$(basename $(PWD)).py
DOCKER_USER ?= jovyan
DOCKER_ENV ?= $(name)

dest_dir ?= /home/$(DOCKER_USER)
volumes ?= -v $$(readlink -f "."):$(dest_dir)
flags ?=
# main.py includes streamlit code that only runs when streamlit invoked
# --restart=unless-stopped  not needed now

## docker: pull docker image and builds locally along with tag with git sha
.PHONY: docker
docker:
	docker build --pull \
				 --build-arg USER=$(DOCKER_USER) \
				 --build-arg NB_USER=$(DOCKER_USER) \
				 --build-arg ENV=$(DOCKER_ENV) \
				 -f $(Dockerfile) \
				 -t $(image) \
				 $(build_path)
	docker tag $(image) $(image):$$(git rev-parse HEAD)
	docker push $(image)

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
