# Use double ## to add specific comments to help
#
# https://www.dataquest.io/blog/docker-data-science/
##
## When running, you will need the juypter notebook token
## access this with `docker logs $(container)`
##
##
#
# Still have issues with stale images
#
# change the variables here
#

# Note that
TAG ?= v2.0
COMMENT ?= test comment

FILES ?= covid-surge-who \
		 covid-surge-who-reed \
		 covid-surge-who-single \
		 covid-surge-who-county \
		 covid-surge-who-single-cook \
		 covid-surge-who-single-ca \
		 covid-surge-who-single-miami

## release: copy up the Excel files to the named locations at the root
.PHONY: release
release:
	@echo if the tag does not exist we skip and use the older version
	for file in $(FILES); do \
		cp "$$file-$(TAG).xlsx" "../$$file.xlsx" || true; \
	done

## action: pushes a new tag up while delete old to force the action
.PHONY: action
action:
	git tag -d "$(TAG)"; \
	git push origin :"$(TAG)" ; \
	git tag -a "$(TAG)" -m "$(COMMENT)" && \
	git push origin "$(TAG)"

include ../lib/include.mk
