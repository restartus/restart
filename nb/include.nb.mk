# consumed by include.python.mk for makes
PIP_DEV+=pre-commit isort
PIP+=h5py confuse \
	  voila voila-reveal voila-vuetify \
	  ipywidgets ipysheet ipympl ipyvolume ipyvuetify  \
	  scipy altair \
	  qgrid bqplot
PIP_ONLY+=restart jupyter-server tables
