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

# Note that this should be the release you want
## TAG: set a tag to the latest release you want
TAG ?= v2.0.2
COMMENT ?= test comment
RELEASE ?= ../release

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
		cp "$$file-$(TAG).xlsx" "$(RELEASE)/$$file.xlsx" || true; \
	done

include ../lib/include.mk
