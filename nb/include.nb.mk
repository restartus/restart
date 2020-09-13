# consumed by include.python.mk for makes
#  nbstripout removes notebook output
PYTHON=3.8.5
PIP_DEV+=pre-commit isort nbstripout
PIP+=h5py confuse \
	  voila voila-reveal voila-vuetify \
	  ipywidgets ipysheet ipympl ipyvolume ipyvuetify  \
	  scipy altair \
	  qgrid bqplot

PIP_ONLY+=restart jupyter-server tables
