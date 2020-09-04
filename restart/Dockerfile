FROM jupyter/base-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
# Using this as the base to get user working right
ARG DOCKER_USER=jovyan
ARG ENV=src

#
# library for docker files
# Desigend for docker files
# https://github.com/gitpod-io/gitpod/tree/master/components/image-builder/workspace-image-layer/gitpod-layer
#
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux



# create_user(user, group, groupuserid)


# src specific for Docker
# https://pythonspeed.com/articles/activate-conda-dockerfile/




# debug tools and sudo need for conda activate
USER root

# Ubuntu debug for docker containers (use with m4)
USER root
RUN mkdir -p /var/lib/apt/lists && apt-get update && \
    apt-get install -y make \
                    vim \
                    sudo \
                    gosu \
                    git && \
    apt-get clean && rm -rf /var/lib/apt/list/*


# make a sudo user
USER root
RUN usermod -aG sudo $DOCKER_USER && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $DOCKER_USER


RUN conda create --name $ENV && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $ENV --quiet --yes \
            python=3.8 \
            pandas confuse ipysheet h5py \
            nptyping pydocstyle pdoc3 flake8 mypy bandit \
            black tox pytest pytest-cov pytest-xdist tox yamllint \
            pre-commit isort seed-isort-config \
            setuptools wheel twine && \
    conda run -n $ENV pip install tables && \
    conda clean -afy && \
    conda init

