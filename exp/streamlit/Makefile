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
## streamlit-install: install for streamlit
.PHONY: streamlit-install
streamlit-install:
	pipenv install opencv-python vega-datasets streamlit altair yfinance pandas
	pipenv update

MAIN = stock.py

## web2: run second apps
.PHONY: web2
web2:
	pipenv run streamlit run cars.py

include ../../../lib/include.model.py
include ../../../lib/include.python.mk
include ../../../lib/include.mk
