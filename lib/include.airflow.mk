#
## User commands:
#
# Remember makefile *must* use tabs instead of spaces so use this vim line
#
# Remember when writing makefile commands, you must use a hard tab and each line
# is run in its own shell, so you cannot pass shell variables between them
# If you want to refer to shell variables, you must make it one virtual line
# http://stackoverflow.com/questions/10121182/multiline-bash-commands-in-makefile
#
# The makefiles are self documenting, you use two leading
# for make help to produce output
#
# These should be overridden in the makefile that includes this, but this sets
# defaults use to add comments when running make help
#
# https://stackoverflow.com/questions/589276/how-can-i-use-bash-syntax-in-makefile-targets
airflow_data ?= $(PWD)
AIRFLOW_PIP ?= apache-airflow mysqlclient datetime tables
AIRFLOW_PIP_DEV ?=
# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916


## airflow-install: configure airflow data directories
# the side effect of airflow version is to create a default airflow.cfg
# Which has the current directory as AIRFLOW_HOME
# Make sure to use a relative path not absolute and .env is checked in!
airflow-install: airflow-pipenv
	# this great must run before any airflow command
	grep ^AIRFLOW_HOME .env || echo AIRFLOW_HOME=. >> .env
	# new safety check in MacOS since Catalina
	grep ^OBJC_DISABLE_INITIALIZE_FORK_SAFETY .env || echo OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES >> .env
	[[ ! -e airflow.cfg ]] && pipenv run airflow version || true
	mkdir -p "$(airflow_data)/dags"
	touch .gitignore
	for file in airflow.cfg airflow.db; \
		do grep $$file .gitignore || echo $$file >> .gitignore; \
		done
	pipenv run airflow initdb


## scheduler: Run the Airflow scheduler (run before the web server)
.PHONY: scheduler
scheduler:
	pipenv run airflow scheduler

## airflow: initialize an airflow web server default port 8080 change with PORT
.PHONY: airflow
PORT?=8080
airflow:
	@echo goto http://localhost:$(PORT) to see console
	pipenv run airflow webserver -p $(PORT)

##
## Installation helpers (you should need to ever call directly):
## airflow-pipenv: install basic environment for airflow
# dependency on include.mk
.PHONY: airflow-pipenv
# override to lower versino
PYTHON = 3.7
airflow-pipenv: airflow-clean pipenv-python
	command -v mysql || brew install mysql-client
	grep mysql-client "$$HOME/.bash_profile" || \
		echo PATH="/usr/local/opt/mysql-client/bin:$$PATH" >> "$$HOME/.bash_profile"
ifdef AIRFLOW_PIP
	pipenv install $(AIRFLOW_PIP)
	pipenv install --dev $(AIRFLOW_PIP_DEV) || true
endif
	pipenv update

## airflow-clean: start over remove all config files
.PHONY: airflow-clean
airflow-clean:
	for file in .env airflow.cfg airflow.db; \
		do \
			[[ -e $$file ]] && rm $$file || true; \
		done
