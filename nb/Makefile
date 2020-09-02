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
# do not need src stuff only notebook
SRC_PIP =
SRC_PIP_DEV =

# For docker config link in key directories
DOCKER_USER ?= jovyan
dest_dir ?= /home/jovyan/ws/restart
flags ?= -p 8888:8888 \
		 -e GRANT_SUDO=1
volumes ?= -v $$(readlink -f "../src"):$(dest_dir)/src \
		   -v $$(readlink -f "../nb"):$(dest_dir)/nb \
		   -v $$(readlink -f "../lib"):$(dest_dir)/lib \
		   -v $$(readlink -f "../config"):$(dest_dir)/config

## ca: edit the California notebook
.PHONY: ca
ca:
	pipenv run jupyter notebook $(CALIFORNIA)

## voila-ca: deployment view of California
.PHONY: voila-ca
voila-ca:
	pipenv run voila $(CALIFORNIA)

## voila-vuetify: Voila demo
.PHONY: voila-vuetify
voila-vuetify:
	pipenv run voila --template=voila-default $(VOILA_DEMO)

## voila-wa: Run Washington Aggregate and Vulnerable Levels
.PHONY: voila-wa
voila-wa:
	pipenv run voila $(VOILA_WA)

VOILA_TEMPLATES ?= $$HOME/Library/Jupyter/voila
# assumes we are submodule
## voila-templates: Make sure we are using our default templates
.PHONY: voila-templates
voila-templates:
	mkdir -p $(VOILA_TEMPLATES)
	rm -rf "$(VOILA_TEMPLATES)/templates"
	ln -s "$(PWD)/voila" "$(VOILA_TEMPLATES)/templates"

## jupyter-wa: Editing the Washington template
.PHONY: jupyter-wa
jupyter-wa:
	pipenv run jupyter notebook $(VOILA_WA)

##

include ../lib/include.docker.mk
include ../lib/include.python.mk
include ../lib/include.mk
