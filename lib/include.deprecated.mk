#
##
## Deprecated commands for make include
# Configure by setting PIP for pip packages and optionally name
# requires include.mk
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading
# for make help to produce output
#
#

## The bare metal python and conda work is deprecated, please use pipenv:
## requirements: Freeze Python requirements in bare machine (deprecated use pipenv)
.PHONY: requirements
requirements:
	@echo WARNING requirements not compatible with pipenv so do not create if using pipenv
	pip freeze > requirements.txt

## bare: install the python packages natively (not recommended (deprecated use pipoenv)
# https://note.nkmk.me/en/python-pip-install-requirements/
.PHONY: bare-install
bare-install:
	pip install -r requirements.txt

##
## conda: create the conda environment run with conda env model (not running for @richtong)
# https://towardsdocker_datascience.com/getting-started-with-python-environments-using-conda-32e9f2779307
.PHONY: conda
conda:
	@echo this installation is note working
	conda env create -f environment.yml
	conda env --list

## conda-activate: run the python environment for model
.PHONY: conda-activate
conda-activate:
	@echo run \"conda activate model\"
