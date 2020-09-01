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

## jupyter-wa: Editing the Washington template
.PHONY: jupyter-wa
jupyter-wa:
	pipenv run jupyter notebook $(VOILA_WA)

##

include ../lib/include.model.mk
include ../lib/include.python.mk
include ../lib/include.mk
