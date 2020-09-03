#
#
##
## Base commands: not language specific
#
TAG ?= v1
# https://www.gnu.org/software/make/manual/make.html#Flavors
# Use simple expansion for most
SHELL :- /bin/bash
repo ?= restartus
name ?= $$(basename "$(PWD)")

.DEFAULT_GOAL := help
.PHONY: help
# https://marmelab.com/blog/2016/02/29/auto-documented-makefile.html does not
# work because we use an include file
# https://swcarpentry.github.io/make-novice/08-self-doc/ is simpler just need
# and it dumpes them out relies on the variable MAKEFILE_LIST which is a list of
# all files note we do not just use $< because this is an include.mk file
## help: available commands (the default)
help: $(MAKEFILE_LIST)
	@sed -n 's/^##//p' $(MAKEFILE_LIST)

## tag: pushes a new tag up while delete old to force the action
.PHONY: tag
tag:
	git tag -d "$(TAG)"; \
	git push origin :"$(TAG)" ; \
	git tag -a "$(TAG)" -m "$(COMMENT)" && \
	git push origin "$(TAG)"

##
## gcloud: push up to Google Cloud
.PHONY: gcloud
gcloud:
	gcloud projects list
