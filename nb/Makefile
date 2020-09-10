#
# https://voila.readthedocs.io/en/stable/deploy.html
# Only need voila for deployment
# Use jupyter ot edit
#
VOILA_WA ?= Washington
VOILA_DEMO ?= VuetifyDemo
CALIFORNIA ?= CaliforniaDash
WASHINGTON ?= Washington
# voila requires jupyter-server 0.1.1
PIPENV_CHECK_FLAGS ?= -i 38212

include include.nb.mk

# For docker config link in key directories
DOCKER_USER ?= jovyan
dest_dir ?= /home/jovyan/workspace
flags ?= -p 8888:8888 \
		 -e GRANT_SUDO=1
volumes ?= -v $$(readlink -f "../restart"):$(dest_dir)/restart \
		   -v $$(readlink -f "../nb"):$(dest_dir)/nb \
		   -v $$(readlink -f "../lib"):$(dest_dir)/lib \
		   -v $$(readlink -f "../config"):$(dest_dir)/config

Dockerfile = Dockerfile
Dockerfile.in = $(Dockerfile).in

$(Dockerfile): $(Dockerfile).in ../lib/lib.docker

## ca: edit the California notebook
.PHONY: ca
ca:
	$(RUN) jupyter notebook $(CALIFORNIA).ipynb

## wa: the current state of Washington notebook default
.PHONY: wa
wa: wa-tf

## wa-tf: the current state of Washington notebook for taskforce
.PHONY: wa
wa-tf:
	$(RUN) jupyter notebook $(WASHINGTON)-taskforce.ipynb

## wa-fema: the current state of Washington notebook for fema
.PHONY: wa-fema
wa-fema:
	$(RUN) jupyter notebook $(WASHINGTON)-fema.ipynb

## wa-fema-slide: Slideshow for Washington FEMA analysis
.PHONY: wa-fema-slide
wa-fema-slide:
	$(RUN) voila --debug --template=reveal $(WASHINGTON)-fema.ipynb

## voila-ca: deployment view of California
.PHONY: voila-ca
voila-ca:
	$(RUN) voila $(CALIFORNIA).ipynb

## voila-vuetify: Voila demo
.PHONY: voila-vuetify
voila-vuetify:
	$(RUN) voila --template=voila-default $(VOILA_DEMO).ipynb

## voila-wa: Run Washington Aggregate and Vulnerable Levels
.PHONY: voila-wa
voila-wa:
	$(RUN) voila $(VOILA_WA).ipynb

## jupyter-wa: Editing the Washington template
.PHONY: jupyter-wa
jupyter-wa:
	$(RUN) jupyter notebook $(VOILA_WA).ipynb

##

include ../lib/include.docker.mk
include ../lib/include.python.mk
include ../lib/include.mk
