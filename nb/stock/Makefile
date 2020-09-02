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
flags ?= -p 8888:8888
volumes ?= -v $$(readlink -f "../../src"):$(dest_dir)/src \
		   -v $$(readlink -f "../../nb"):$(dest_dir)/nb \
		   -v $$(readlink -f "../../lib"):$(dest_dir)/lib \
		   -v $$(readlink -f "../../config"):$(dest_dir)/config

include ../../lib/include.docker.mk
include ../../lib/include.python.mk
include ../../lib/include.mk
