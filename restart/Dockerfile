FROM jupyter/base-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
# Using this as the base to get user working right
ARG DOCKER_USER=jovyan
ENV CONDA_ENV=restart

# This is set for make files of restart
#

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


RUN conda create --name $CONDA_ENV && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $CONDA_ENV --quiet --yes \
            python=3.8 \
            pandas confuse ipysheet h5py  \
            nptyping pydocstyle pdoc3 flake8 mypy bandit \
            black tox pytest pytest-cov pytest-xdist tox yamllint \
            pre-commit isort seed-isort-config \
            setuptools wheel twine && \
    conda run -n $CONDA_ENV pip install tables && \
    conda clean -afy && \
    conda init


USER $DOCKER_USER
RUN echo "export ENV=conda" >> "$HOME/.bashrc" && \ 
    conda init && \
    echo "conda activate restart" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate restart

