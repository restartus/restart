<<<<<<< HEAD
## run Voila

# https://voila.readthedocs.io/en/stable/deploy.html
#
# Only need voila
#
## voila-wa: Run Washington Aggregate and Vulnerable Levels
VOILA_WA ?= Washington.ipynb

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
