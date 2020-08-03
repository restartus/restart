#
# Makefile tuned for Python and Streamlit
#
# overriding the name
name=model
FLAGS = --load yaml --pop dict
CA_FLAGS = --load yaml --pop oes --state California --demand washington --subpop healthcare
MAIN = main.py

include ../lib/include.mk
include ../lib/include.python.mk
include ../lib/include.model.mk
include ../lib/include.docker.mk
