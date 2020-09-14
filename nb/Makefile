#
# https://voila.readthedocs.io/en/stable/deploy.html
# Only need voila for deployment
# Use jupyter ot edit
#
VOILA_WA ?= Washington
VOILA_DEMO ?= VuetifyDemo
CALIFORNIA ?= CaliforniaDash
CA_PPE ?= CaliforniaPPE
WASHINGTON ?= Washington
# voila requires jupyter-server 0.1.1
PIPENV_CHECK_FLAGS ?= -i 38212

include include.nb.mk

# For docker config link in key directories
DOCKER_USER ?= jovyan
dest_dir ?= /home/jovyan/workspace
flags ?= -p 8888:8888 \
		 -e GRANT_SUDO=1
volumes ?= -v $$(readlink -f ".."):$(dest_dir)/restart
		   # -v $$(readlink -f "../nb"):$(dest_dir)/nb \
		   # -v $$(readlink -f "../lib"):$(dest_dir)/lib \
		   # -v $$(readlink -f "../config"):$(dest_dir)/config

Dockerfile = Dockerfile
Dockerfile.in = $(Dockerfile).in

$(Dockerfile): $(Dockerfile).in ../lib/lib.docker
## ca: the default california analysis
.PHONY: ca
ca: ca-ppe

## ca-slide: the default California slide show
.PHONY: ca-slide
ca-slide: ca-ppe-slide

## ca-ppe: PPE analysis for California
.PHONY: ca-ppe
ca-ppe:
	$(RUN) jupyter notebook CaliforniaPPE.ipynb

## ca-ppe-slide: Slide show for PPE California
.PHONY: ca-ppe-slide
ca-ppe-slide:
	$(RUN) voila --template=vuetify-default CaliforniaPPE.ipynb
	$(RUN) voila --template=reveal CaliforniaPPE.ipynb


## ca-dash: edit the California notebook dashboard
.PHONY: ca-dash
ca-dash:
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

## voila-ca: deployment view of California
.PHONY: voila-ca
voila-ca:
	$(RUN) voila $(CALIFORNIA).ipynb

## ca-slides: California slideshow with voila-reveal
.PHONY: ca-slides
ca-slides:
	$(RUN) voila $(CALIFORNIA).ipynb --template=reveal

## ca-ppe-slides: CaliforniaPPE slideshow with voila-reveal
.PHONY: ca-ppe-slides
ca-ppe-slides:
	$(RUN) voila $(CA_PPE).ipynb --template=reveal

## wa-fema-slides: Washington-fema slideshow with voila-reveal
.PHONY: wa-fema-slides
wa-fema-slides:
	$(RUN) voila $(WASHINGTON)-fema.ipynb --template=reveal

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
