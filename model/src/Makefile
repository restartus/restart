#
# Makefile tuned for Python and Streamlit
#
# overriding the name
name=model
FLAGS = --pop dict
CA_FLAGS = --pop oes --state California --demand washington --subpop healthcare
WA_FLAGS = --pop wa --demand washington
MAIN = main.py

include ../lib/include.mk
include ../lib/include.python.mk
include ../lib/include.model.mk
include ../lib/include.docker.mk
