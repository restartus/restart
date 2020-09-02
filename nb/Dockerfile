FROM jupyter/scipy-notebook
LABEL maintainer="Restart Us <admin@restart.us>"

# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-pip-install-or-conda-install-in-a-child-docker-image
# Use conda but some things are only in pip
# https://conda-forge.org/#about
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --quiet --yes \
                voila \
                confuse \
                ipysheet \
                bqplot \
                ipyvuetify \
                voila-vuetify

WORKDIR /home/jovyan/work/nb
