# Use double ## to add specific comments to help
#
# https://www.dataquest.io/blog/docker-data-science/
##
## When running, you will need the juypter notebook token
## access this with `docker logs $(container)`
## 
##
#
# Still have issues with stale images
#
# change the variables here
repo ?= restartus
name ?= $$(basename "$(PWD)")
Dockerfile ?= Dockerfile
image ?= $(repo)/$(name)
container = $(name)
# this is data in the container that links to the outside work
# This is the default for all Jupyter containers
data ?= /home/jovyan
host_data ?= $$PWD/data
destination ?= $(HOME)/ws/runtime
# the user name on the host nodes if a raspberry pi
user ?= anaconda

## install: for bare metal installs installs Python packages
install:
	pip install --upgrade opencv-python vega-datasets streamlit altair

## gcloud: push up to Google Cloud
gcloud:
	gcloud projects list

# /dev/video0 needed for v4l2
# /dev/vchiq needed for mmal
# Punch the image directory out to the host. We are doing this because docker cp
# is way too slow
# port 5858 is the node debug port
# For some reason the src mapping no long works you cannot map
# probably for security reasons only hard files below the level of the current
# directory can to bind mounted
# -v $(PWD)/src:/home/$(user)/src 
# port 22 is ssh
# -p 22:22
# port 8888 is jupyter output port
flags ?= -p 8888:8888  \
		 --mount type=bind,source=$(host_data),target=$(data)

## prebuild: runs the base docker container
prebuild:
					cd ../../../extern/jupyter-docker-stacks/ && \
					make build/tensorflow-notebook OWNER=$(repo) && \
					docker push $(repo)/tensorflow-notebook

include include.mk
