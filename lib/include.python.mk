#
# mainMinimal include (does not include docker commands
#
# Remember makefile *must* use tabs instead of spaces so use this vim line
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading ## for make help to
# produce output
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use ## to add comments when running make help
# 
# Two entry points in MAIN and WEB
repo ?= restartus
name ?= $$(basename "$(PWD)")
Dockerfile ?= Dockerfile
image ?= $(repo)/$(name)
container = $(name)
data ?= /var/media
destination ?= $(HOME)/ws/runtime
# the user name on the host nodes if a raspberry pi
user ?= $$USER
# If you need the infra/bin tools, then you need to set the build to run
# relatively there
build_path ?= .
user ?= $$USER
MAIN ?= main.py
WEB ?= dashboard.py
flags ?= -p 8501:8501

.DEFAULT_GOAL := help

.PHONY: help
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need ##
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file 
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)

##
## pipenv based running (for debugging)
## ------------------------------------
## web: use streamlit to run the graphical interface
.PHONY: web
web:
	pipenv run streamlit run $(WEB)

# https://pipenv.pypa.io/en/latest/install/
# https://realpython.com/pipenv-guide/
# install everything including things just needed for edevelopment
## pipenv: Install with pipenv as virtual environment
.PHONY: pipenv
pipenv:
	@echo you should install with pip install pipenv and then pipenv shell
	pipenv install --dev

## pypi: push the package to the Python library
.PHONY: pypi
pypi:
	pipenv run python setup.py register -r pypi
	pipenv run python setup.py sdit upload -r pypi

## test: run static tests
.PHONY: test
test:
	pipenv check
	pipenv run flake8
	pipenv run bandit -r $(MAIN)
	pipenv run bandit -r $(WEB)
	# pipenv run black -l 79 *.py
	@echo if you want destructive formatting run black *.py
	@echo or for pipenv black -l 79 *.py

##
## The bare metal python and conda work is deprecated, please use pipenv
## ---------------------------------------------------------------------
## main: run locally with python to test components from main (deprecated use pipenv)
.PHONY: main
main:
	python $(MAIN)

# https://docs.python.org/3/library/pdb.html
## pdb: run locally with python to test components from main (depreceated use pipenv)
.PHONY: pdb
pdb:
	python -m pdb $(MAIN)

## web-pdb: run web interface in debugger
web-pdb:
	python -m pdb $(WEB)


## requirements: Freeze Python requirements in bare machine (deprecated use pipenv)
.PHONY: requirments
requirements:
	pip freeze > requirements.txt

## bare: install the python packages natively (not recommended (deprecated use pipoenv)
# https://note.nkmk.me/en/python-pip-install-requirements/
.PHONY: bare
bare:
	pip install -r requirements.txt

##
## conda: create the conda environment run with conda env model (not running for @richtong)
# https://towardsdatascience.com/getting-started-with-python-environments-using-conda-32e9f2779307
.PHONY: conda
conda:
	@echo this installation is note working
	conda env create -f environment.yml
	conda enc --list

## conda-activate: run the python environment for model
.PHONY: conda-activate
conda-activate:
	@echo run \"conda activate model\"

##
## docker installation (for deployments)
## -------------------------------------
## docker: pull docker image and builds locally along with tag with git sha
docker: 
	docker build --pull --build-arg USER=$(user) -f $(Dockerfile) -t $(image) .
	docker tag $(image) $(image):$$(git rev-parse HEAD)

## push: after a build will push the image up
push: build  
	# need to push and pull to make sure the entire cluster has the right images
	docker push $(image)

# for those times when we make a change in but the Dockerfile does not notice
# In the no cache case do not pull as this will give you stale layers
## nocache: does not use docker hub prevent stale layers from being downloaded
no-cache:
	docker build --no-cache --build-arg USER=$(user) -f $(Dockerfile) -t $(image) .
	docker push $(image)
	docker pull $(image)

for_containers = bash -c 'for container in $$(docker ps -a | grep "$$0" | awk "{print \$$NF}"); \
						  do \
						  	echo docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  	docker $$1 "$$container" $$2 $$3 $$4 $$5 $$6 $$7 $$8 $$9; \
						  done'

## stop: halts all running containers
stop:
	@$(for_containers) $(container) stop
	@$(for_containers) $(container) "rm -v" 

## pull: pulls the latest image
pull:
	docker pull $(image)

# you do not want to clean but `make run` as many times as you have cluster
# members
# https://github.com/docker/docker/issues/2838 so we need the -t so that we can
# ctrl-C it. To see containers, you need to run `docker exec -it $(container)`
# To see the exact console output `docker attach $(container)` and you need the
# -i flag otherwise you cannot ctrl-c out of it
#  To restart a dead container with interactive, you need `docker start -ai
#  $(container)
#  -t means assign a consoler tty to it, -i means keep it interactive and attach
#  stdin and stdout 
# when deploying we do not want to stop running containers
# And we want to use random names with a two digit extension
# Make sure to use the -t so you can stop it
## docker-run: build then push up then run the image
docker-run: push pull run-local

## run-local: stops all the containers and then runs one locally
# docker pull $(image)
# Find the last container number
# Find the next free container name
# https://jpetazzo.github.io/2015/01/19/dockerfile-and-data-in-volumes/
# Remove the -v $(data) will take it out of the COW file system
# pass down the current USER
run-local: stop
	last=$$(docker ps | grep $(image) | awk '{print $$NF}' | cut -d/ -f2 | awk 'BEGIN { FS="-" }; {print $$NF}' | sort -r | head -n1) ; \
	echo last found is $$last ; \
	docker run -dt --restart=unless-stopped --name $(container)-$$((last+1)) $(flags) $(image)
	# show the logs because for some you need to know the url for the web server as with anaconda
	docker logs $(container)-$$((last+1))

shell: push pull stop
	docker pull $(image)
	docker run -it $(flags) --name $(container) $(image) bash

## debug: interactive but do not pull for use offline
debug: stop
	@docker run -it $(flags) --name $(container) $(image) bash


## resume: keep running an existing container
resume: 
	docker start -ai $(container)

# Note we say only the type file because otherwise it tries to delete $(data) itself
## rm-images: remove docker images
rm-images:
	$(for_containers) $(container) exec find $(data) -type f -delete

##
# https://medium.com/@Tankado95/how-to-generate-a-documentation-for-python-code-using-pdoc-60f681d14d6e
## doc: make the documentation for the Python project
##
.PHONY: doc
doc:
	cd .. && PYTHONPATH="." pdoc --html src --output-dir docs
