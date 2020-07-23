#
## Run this after you have includded include.python.mk
## Specific to running airflow
##
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
AIRFLOW_PIP ?= apache-airflow mysqlclient datetime
# https://www.gnu.org/software/make/manual/html_node/Splitting-Lines.html#Splitting-Lines
# https://stackoverflow.com/questions/54503964/type-hint-for-numpy-ndarray-dtype/54541916


## airflow-install: configure airflow data directories
# the side effect of airflow version is to create a default airflow.cfg
# Which has the current directory as AIRFLOW_HOME
airflow-install: install
	@echo add /usr/local/opt/mysql-client/bin
	[[ ! -e airflow.cfg ]] && airflow version || true
	grep AIRFLOW_HOME .env || echo AIRFLOW_HOME="$(airflow_data)" > .env
	mkdir -p "$(airflow_data)/dags"
	for file in airflow.cfg airflow.db; \
		do grep $$file .gitignore || echo $$file >> .gitignore; \
		done
	pipenv run airflow initdb

## airflow: initialize an airflow db
.PHONY: airflow
airflow:
	pipenv run airflow webserver &
	sleep 3
	open http://localhost:8080

## scheduler: Run the Airflow scheduler
.PHONY: scheduler
scheduler:
	pipenv run airflow scheduler
