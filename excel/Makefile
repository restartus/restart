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

tag =? v1.4.7.2
## release: copy up the Excel files to the named locations at the root
files =?  covid-surge-who-county.xlsx covid-surge-who-single-cook.xlsx covid-surge-who-single.xlsx covid-surge-who.xlsx

.PHONY: install
install: 
	for file in $(files); do \
		cp "$$file-$(tag)" "../$$file"; \
	done

include include.mk
