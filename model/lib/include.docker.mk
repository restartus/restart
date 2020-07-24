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
docker_data ?= /var/media
destination ?= $(HOME)/ws/runtime
build_path ?= .
MAIN ?= $$(basename $(PWD)).py
# main.py includes streamlit code that only runs when streamlit invoked
WEB ?= $(MAIN)
LIB ?= lib
NO_WEB ?= $$(find . -maxdepth 1 -name "*.py"  -not -name $(WEB))
flags ?= -p 8501:8501


## docker: pull docker image and builds locally along with tag with git sha
docker:
	docker build --pull --build-arg USER=$(user) -f $(Dockerfile) -t $(image) .
	docker tag $(image) $(image):$$(git rev-parse HEAD)

## push: after a build will push the image up
push: build
	# need to push and pull to make sure the entire cluster has the right images
	docker push $(image)

# for those times when we make a change in but the Dockerfile does not notice
# In the no cache case do not pull as this will give you stale layers
## nocache: does not use docker hub prevent stale layers from being downloaded
no-cache:
	docker build --no-cache --build-arg USER=$(user) -f $(Dockerfile) -t $(image) .
	docker push $(image)
	docker pull $(image)

for_containers = bash -c 'for container in $$(docker ps -a | grep "$$0" | awk "{print \$$NF}"); \
						  do \
						  	echo docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  	docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  done'

## stop: halts all running containers
stop:
	@$(for_containers) $(container) stop
	@$(for_containers) $(container) "rm -v"

## pull: pulls the latest image
pull:
	docker pull $(image)

# you do not want to clean but `make run` as many times as you have cluster
# members
# https://github.com/docker/docker/issues/2838 so we need the -t so that we can
# ctrl-C it. To see containers, you need to run `docker exec -it $(container)`
# To see the exact console output `docker attach $(container)` and you need the
# -i flag otherwise you cannot ctrl-c out of it
#  To restart a dead container with interactive, you need `docker start -ai
#  $(container)
#  -t means assign a consoler tty to it, -i means keep it interactive and attach
#  stdin and stdout
# when deploying we do not want to stop running containers
# And we want to use random names with a two digit extension
# Make sure to use the -t so you can stop it
## docker-run: build then push up then run the image
docker-run: push pull run-local

## run-local: stops all the containers and then runs one locally
# docker pull $(image)
# Find the last container number
# Find the next free container name
# https://jpetazzo.github.io/2015/01/19/dockerfile-and-data-in-volumes/
# Remove the -v $(docker_data) will take it out of the COW file system
# pass down the current USER
run-local: stop
	last=$$(docker ps | grep $(image) | awk '{print $$NF}' | cut -d/ -f2 | awk 'BEGIN { FS="-" }; {print $$NF}' | sort -r | head -n1) ; \
	echo last found is $$last ; \
	docker run -dt --restart=unless-stopped --name $(container)-$$((last+1)) $(flags) $(image)
	# show the logs because for some you need to know the url for the web server as with anaconda
	docker logs $(container)-$$((last+1))

shell: push pull stop
	docker pull $(image)
	docker run -it $(flags) --name $(container) $(image) bash

## docker-debug: interactive but do not pull for use offline
docker-debug: stop
	@docker run -it $(flags) --name $(container) $(image) bash

## resume: keep running an existing container
resume:
	docker start -ai $(container)

# Note we say only the type file because otherwise it tries to delete $(docker_data) itself
## rm-images: remove docker images
rm-images:
	$(for_containers) $(container) exec find $(docker_data) -type f -delete
