#
# https://voila.readthedocs.io/en/stable/deploy.html
# Only need voila for deployment
# Use jupyter ot edit
#
VOILA_WA ?= Washington.ipynb
VOILA_DEMO ?= VuetifyDemo.ipynb
CALIFORNIA ?= CaliforniaDash.ipynb
# voila requires jupyter-server 0.1.1
PIPENV_CHECK_FLAGS ?= -i 38212

# consumed by include.python.mk for makes
PIP_DEV = pre-commit isort
PIP = voila ipywidgets ipysheet qgrid bqplot ipympl ipyvolume ipyvuetify voila-vuetify \
		  scipy confuse voila-reveal
PIP_ONLY = jupyter-server

# For docker config link in key directories
DOCKER_USER ?= jovyan
dest_dir ?= /home/jovyan/ws/restart
flags ?= -p 8888:8888 \
		 -e GRANT_SUDO=1
volumes ?= -v $$(readlink -f "../src"):$(dest_dir)/src \
		   -v $$(readlink -f "../nb"):$(dest_dir)/nb \
		   -v $$(readlink -f "../lib"):$(dest_dir)/lib \
		   -v $$(readlink -f "../config"):$(dest_dir)/config

Dockerfile = Dockerfile
Dockerfile.in = $(Dockerfile).in
$(Dockerfile): $(Dockerfile).in ../lib/lib.docker nb.docker

## ca: edit the California notebook
.PHONY: ca
ca:
	$(RUN) jupyter notebook $(CALIFORNIA)

## voila-ca: deployment view of California
.PHONY: voila-ca
voila-ca:
	$(RUN) voila $(CALIFORNIA)

## voila-vuetify: Voila demo
.PHONY: voila-vuetify
voila-vuetify:
	$(RUN) voila --template=voila-default $(VOILA_DEMO)

## voila-wa: Run Washington Aggregate and Vulnerable Levels
.PHONY: voila-wa
voila-wa:
	$(RUN) voila $(VOILA_WA)

## jupyter-wa: Editing the Washington template
.PHONY: jupyter-wa
jupyter-wa:
	$(RUN) jupyter notebook $(VOILA_WA)

##

include ../lib/include.docker.mk
include ../lib/include.python.mk
include ../lib/include.mk
