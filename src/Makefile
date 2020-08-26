#
# Makefile tuned for Python and Streamlit
#
# overriding the name
TAG ?= v2.3
name=model
FLAGS = --pop dict
CA_FLAGS = --pop oes --state California --subpop healthcare
WA_FLAGS = --pop wa --demand washington
MAIN = main.py

include ../lib/include.mk
include ../lib/include.python.mk
include ../lib/include.model.mk
include ../lib/include.docker.mk

## config-gen create config yaml files
.PHONY: config-gen
config-gen:
	pipenv run python main.py --pop oes --state Indiana --county "St. Joseph" --output ../config/sj/config.yaml
	pipenv run python main.py --pop wa --output ../config/wa/config.yaml
