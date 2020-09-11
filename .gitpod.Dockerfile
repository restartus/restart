# this install is different from
FROM continuumio/miniconda3 as continuum
# this has the incorrect install and just grabs latest
# It also has an error in install where it says /opt/conda but is really
# /usr/local
# FROM conda/miniconda3 AS conda
FROM restartus/restart AS restart

FROM gitpod/workspace-full
LABEL maintainer="Restart Us <admin@restart.us>"
# Set environment for setup
ARG CONDA_ENV=restart
# must use numbers for this gitpod override in makefile
ARG DOCKER_USER=gitpod
ARG DOCKER_UID=33333

# To be used in gitpod.io must be debian/ubuntu or alpine based
# Must also have a gitpod use
# With the jupyter/scipy-notebook base we end up with two users
# gitpod and joyvan
# This is set for make files of restart
#
# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/
# remember very argument needs to be declared in Docker
ARG PYTHON
ARG PACKAGES
ARG PIP
ARG PIP_ONLY
# These are for development time
ARG PIP_DEV



#
# https://github.com/gitpod-io/gitpod/tree/master/components/image-builder/workspace-image-layer/gitpod-layer
#
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux





# create_user(user, group, groupuserid)


# set_env(user,conda-env)





# if you can figure out where apt-get installs
# this could also become
# FROM restart/debug AS debug
# Then in the current container
# COPY --from=debug /usr/bin /usr/bin
# https://peteris.rocks/blog/quiet-and-unattended-installation-with-apt-get/
USER root
RUN mkdir -p /var/lib/apt/lists && apt-get update && \
    DEBIAN_FRONTEND=noninteractive apt-get install -qq \
                    make \
                    vim \
                    sudo \
                    gosu \
                    git \
                    && \
    apt-get clean && rm -rf /var/lib/apt/list/*


# Testing copies this currently generates an error
# because the current miniconda puts things in the wrong place
# COPY --from=conda /opt/conda /opt/conda-from
COPY --chown=gitpod:gitpod --from=continuum /opt/conda /opt/conda
ENV PATH /opt/conda/bin:$PATH
RUN mkdir -p /opt/restart/bin
COPY --chown=gitpod:gitpod --from=restart /usr/bin/make /opt/restart/bin
COPY --chown=gitpod:gitpod --from=restart /usr/bin/vi /opt/restart/bin
COPY --chown=gitpod:gitpod --from=restart /usr/sbin/gosu /opt/restart/bin

USER gitpod
ENV PATH /opt/conda/bin:$PATH
RUN conda env list | grep "^$CONDA_ENV" || conda create --name $CONDA_ENV
RUN \
    echo env=$CONDA_ENV python=$PYTHON pip=$PIP pip_only=$PIP_ONLY && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $CONDA_ENV --quiet --yes python=$PYTHON \
                $PIP && \
    conda run -n $CONDA_ENV pip install \
                $PIP_ONLY && \
    conda clean -afy && \
    conda init



USER gitpod
ENV HOME=/home/gitpod
RUN conda env list && \
    echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate $CONDA_ENV" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate $CONDA_ENV


WORKDIR /home/gitpod/workspace
USER gitpod
