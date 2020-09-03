FROM jupyter/base-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
# Using this as the base to get user working right
ARG DOCKER_USER=jovyan
ARG ENV=src



# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh



# taken from $1


# src specific for Docker
# https://pythonspeed.com/articles/activate-conda-dockerfile/




# debug tools and sudo need for conda activate
USER root

# Ubuntu debug for docker containers (use with m4)
RUN apt-get update && \
    apt-get install -y make \
                    vim \
                    sudo \
                    git && \
    apt-get clean && rm -rf /var/lib/apt/list/*


# make a sudo user
USER root
RUN usermod -aG sudo $DOCKER_USER && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $DOCKER_USER
RUN sudo ls


RUN conda create --name $ENV && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $ENV --quiet --yes \
            python=3.8 \
            pandas confuse ipysheet \
            nptyping pydocstyle pdoc3 flake8 mypy bandit \
            black tox pytest pytest-cov pytest-xdist tox yamllint \
            pre-commit isort seed-isort-config \
            setuptools wheel twine && \
    conda run -n $ENV pip install tables && \
    conda clean -afy && \
    conda init
