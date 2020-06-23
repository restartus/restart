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
.PHONY: install
install:
	pip install --upgrade opencv-python vega-datasets streamlit altair

## gcloud: push up to Google Cloud
.PHONY: gcloud
gcloud:
	gcloud projects list

include include.python.mk
