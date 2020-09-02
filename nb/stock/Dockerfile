FROM jupyter/scipy-notebook
LABEL maintainer="Restart Us <admin@restart.us>"

# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-pip-install-or-conda-install-in-a-child-docker-image
# Use conda but some things are only in pip
# https://conda-forge.org/#about
USER $DOCKER_USER
# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/
RUN conda create --name $ENV && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $ENV --quiet --yes \
            numpy \
            pandas \
            pyomo \
    conda run -n $ENV pip install \
            gurobipy && \
    conda clean -afy && \
    conda init

WORKDIR /home/jovyan/ws/restart
