FROM jupyter/scipy-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
ARG DOCKER_USER=jovyan
ARG ENV=nb

# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-pip-install-or-conda-install-in-a-child-docker-image
# Use conda but some things are only in pip
# https://conda-forge.org/#about

# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
USER root
RUN usermod -aG sudo $DOCKER_USER && \
    echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER $DOCKER_USER
# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/
RUN conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --quiet --yes \
                voila \
                confuse \
                ipysheet \
                bqplot \
                ipyvuetify \
                voila-reveal
                && \
    pip install \
                tables \
                && \
    conda clean -afy && \
    conda init

# Cannont conda activate so instead just clone
RUN conda create --name $ENV --clone base

WORKDIR /home/jovyan/ws/restart
