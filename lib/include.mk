# Remember makefile *must* use tabs instead of spaces so use this vim line
# We always push to keep docker in sync
# We need to make sure not to expand tabs as make is tab sensitive
# vi: set tabstop=4 shiftwidth=4 noexpandtab
#
# Still have issues with stale images so be careful
# Now uses include.mk to get the common Makefile elements
#
# change the variables here and override with `make repo=foo`
# http://stackoverflow.com/questions/2826029/passing-additional-variables-from-command-line-to-make
# Note the ?= means only set if not done in the environment
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading ## for make help to
# produce output
#
# Makefile for containerized images allows multiple running instances
# When used with docker-machine you can run in swarms
#
# There are local only commands as well as commands that require and internet connection
#
#
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use ## to add comments when running make help
##
repo ?= restartus
name ?= $$(basename "$(PWD)")
Dockerfile ?= Dockerfile
image ?= $(repo)/$(name)
container = $(name)
data ?= /var/media
destination ?= $(HOME)/ws/runtime
# the user name on the host nodes if a raspberry pi
user ?= $$USER
# If you need the infra/bin tools, then you need to set the build to run
# relatively there
build_path ?= .

#hosts ?= foo
#hosts ?= $(shell echo foo)
# This uses ip addresses but not convenient for naming
#  hosts ?= $$(docker info | grep ":2376" | cut -d":" -f 2 | sed -e "s/^ */$(user)@/" )
#  Get the host names and adds .local for avahi names
#  Note that these substitutions are textual and the bash command is *not*
#  evaluated here
hosts ?= $$( docker info | grep 2376 | cut -d: -f1 | tr -d ' ')

# The docker swarm master if any and the token
master ?= $(docker ps | grep swarm-agent-master | awk '{print $$NF}')

# The docker swarm master if any and the token
# master ?= $(docker ps | grep swarm-agent-master | awk '{print $$NF}')
# token ?= $(docker inspect $(master) | grep token | head -1)
token ?= $(docker inspect $(master) | grep token | head -1)

# /dev/video0 needed for v4l2
# /dev/vchiq needed for mmal
# Punch the image directory out to the host. We are doing this because docker cp
# is way too slow
# flags ?= --device /dev/vchiq -p 80:8080 -p 8081:8081 -v /var/images:/var/images

# Run on a container if it exists and not $NF in awk is number of fields so give
# usage for_containers container docker-action
for_containers = bash -c 'for container in $$(docker ps -a | grep "$$0" | awk "{print \$$NF}"); \
						  do \
						  	echo docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  	docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  done'

# usage cp_containers container source destination
cp_containers = bash -c 'for container in $$(docker ps -a | grep "$$0" | awk "{print \$$NF}"); \
						 do \
						 	echo "making $$2/$$container"; \
						 	mkdir -p "$$2/$$container"; \
							echo "copying $$container:$$1"; \
						 	docker cp "$$container:$$1" "$$2/$$container"; \
						 done'


# These do not generate artifacts but are really commands
.PHONY: build no-cache stop shell run run-all copy slow-copy rm-images text push help debug pull

.DEFAULT_GOAL := help

# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need ##
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file 
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)


## requirements: Freeze Python requirements in bare machine
requirements:
	pip freeze > requirements.txt

## build: pull docker image and builds locally along with tag with git sha
build: 
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
## run: build then push up then run the image
run: push pull run-local

## run-local: stops all the containers and then runs one locally
# docker pull $(image)
# Find the last container number
# Find the next free container name
# https://jpetazzo.github.io/2015/01/19/dockerfile-and-data-in-volumes/
# Remove the -v $(data) will take it out of the COW file system
# pass down the current USER
run-local: stop
	last=$$(docker ps | grep $(image) | awk '{print $$NF}' | cut -d/ -f2 | awk 'BEGIN { FS="-" }; {print $$NF}' | sort -r | head -n1) ; \
	echo last found is $$last ; \
	docker run -dt --restart=unless-stopped --name $(container)-$$((last+1)) $(flags) $(image)
	# show the logs because for some you need to know the url for the web server as with anaconda
	docker logs $(container)-$$((last+1))

## run-all: keep starting containers until docker says no more can be run (used for swarms)
run-all: pull stop
	#if [[ -z $(master) ]]; then exit 0; fi
	#total=$(docker info | grep Nodes | awk '{print $NF}')
	node=0 ; \
	while docker run -dt --restart=unless-stopped --name $(container)-$$node $(flags) $(image) ; \
	do \
		((node+=1)) ;\
	done


# note that circleci uses docker 1.8 so does not support --restart and we do not
# need for tests that is the main difference with `make run`
## test: (obsolete) target for circleci when it was using docker 1.8 for ci tests now use the run target
test: pull
	last=$$(docker ps | grep $(image) | awk '{print $$NF}' | cut -d/ -f2 | awk 'BEGIN { FS="-" }; {print $$NF}' | sort -r | head -n1) ; \
	echo last found is $$last ; \
	docker run -dt --name $(container)-$$((last+1)) $(flags) $(image)

## shell: interactive testing build the image, freshen docker and then run interactively
shell: push pull stop
	docker pull $(image)
	docker run -it $(flags) --name $(container) $(image) bash

## debug: interactive but do not pull for use offline
debug: stop
	@docker run -it $(flags) --name $(container) $(image) bash


## resume: keep running an existing container
resume: 
	docker start -ai $(container)

	# the list does not work for this swarm, so use alternative method
	# hosts=$(docker run --rm hypriot/rpi-swarm list "$(token) | cut -d: -f 1)
	# look for socket the magic socket
	# note for some reason $() and `` do not work here so use a makefile
	# variable
	# hosts=`docker info | awk -F: "/:2376/ {print \"$(user)@\"\$$1\".local\"}" | tr -d ' ' `
	# Note the difference between make variables iusing $() and bash variables # with the $$
	# We also only use the ip addresses that we get
	# Note we use find and move instead of mv because the number of files can
	# exceed the shell line limit
	# Using docker-machine scp  instead of having to know the user name and
	# .local
    # scp -r "$(user)@$$host_ip.local:$(data)/*" "$(destination)/$$host"; \
		# Because scp does not wild card and we can have lots and lots images
	# which exceed the bash command line length, we use find to move the files
	# The find line looks strange because you need both a semicolon to end the
	# find and a semicolon for bash
	# Then switch to rsync as it is more efficient and does not need find
	# rsync -a --remove-source-files "$$scp_target/" "$$host_dst" ; \
	# Note we need the trailng slash so it refers to all files in hte directory
	# But this is intensive as it does copy files
	# So switch back to mv -b which makes a backup if the file exists

## copy: copy the contents of the container data out with docker-machine scp
copy:
	echo copying from $(hosts) to $(destination)
	for host in $(hosts);\
	do \
		echo processing $$host ;\
		host_dst="$(destination)/$$host" ;\
		scp_target="$$host_dst/$$(basename $(data))" ;\
		mkdir -p "$$host_dst" ;\
		docker-machine scp -r "$$host:$(data)" "$$host_dst";\
		find "$$scp_target" -type f -exec mv -b {} "$$host_dst" \; ;\
		rm -r "$$scp_target";\
	done

## slow-copy: deprecated, this uses a simple cp rather than docker-machine
slow-copy:
	: extract videos and stills from containers (warning very very slow 300KBps)
	$(cp_containers) $(container) images "$(destination)"

## other-copies: deprecated this is yet another copy method
other-copies:
	# This requires a secret in the container to authenticate we really want to
	# do it the other way around Here are some methods and why we did not use
	# them:
	#
	# This works only if the container has a private ssh key to the $(destination)
	# $(for_containers) $(container) exec scp -r $(data) $(destination)
	#
	# We need an ftp server to make this work and of course the permissions are
	# in clear text
	# http://stackoverflow.com/questions/14019890/uploading-all-of-files-in-my-local-directory-with-curl
	# $(for_containers) $(container) exec find $(data) -type f -u username:password -exec curl --ftp-create-dirs -T {} ftp://thor.local/zfs_data/$(container)/{}
	#
	# We need an http server for this to work but it would work across the
	# network
	# https://curl.haxx.se/docs/httpscripting.html#PUT
	# $(for_containers) $(container) exec find $(data) -type f -exec curl --upload-file {} http://thor.local/upload

# we use find because there can be so many images that we exceed the command line
#$(for_containers) $(container) exec rm -rf $(data)/*
# Note we say only the type file because otherwise it tries to delete $(data) itself
rm-images:
	$(for_containers) $(container) exec find $(data) -type f -delete

##
##
