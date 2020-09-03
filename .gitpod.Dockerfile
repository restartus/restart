FROM gitpod/workspace-full
LABEL maintainer="Restart Us <admin@restart.us>"
# Using this as the base to get user working right
ARG DOCKER_USER=jovyan
ARG GITPOD_USER=gitpod
ARG ENV=src

USER root
# From  https://hub.docker.com/r/continuumio/miniconda/dockerfile
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get update --fix-missing && \
    apt-get install -y wget bzip2 ca-certificates curl git && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-4.5.11-Linux-x86_64.sh -O ~/miniconda.sh && \
    /bin/bash ~/miniconda.sh -b -p /opt/conda && \
    rm ~/miniconda.sh && \
    /opt/conda/bin/conda clean -tipsy && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

ENV TINI_VERSION v0.16.1
ADD https://github.com/krallin/tini/releases/download/${TINI_VERSION}/tini /usr/bin/tini
RUN chmod +x /usr/bin/tini

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

# from https://hub.docker.com/r/gitpod/workspace-full/dockerfile
RUN if ! id $GITPOD_USER; then useradd -l -u 33333 -G sudo -md /home/$GITPOD_USER \
    -s /bin/bash -p $GITPOD_USER $GITPOD_USER; fi && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/$GITPOD_USER

# https://medium.com/@chadlagore/conda-environments-with-docker-82cdc9d25754
# RUN conda create -n src python=3.8 && \
    #     echo "source activate src" > ~/.bashrc \
    # ENV PATH /opt/conda/env/src/bin:$PATH

# https://jupyter-docker-stacks.readthedocs.io/en/latest/using/recipes.html#using-pip-install-or-conda-install-in-a-child-docker-image
# Use conda but some things are only in pip
# https://conda-forge.org/#about
#
# to make tings smllaer
# https://jcristharif.com/conda-docker-tips.html

# need a way to include in Dockerfiles
# debug tools and sudo need for conda activate
USER root
RUN apt-get update && \
    apt-get install -y make \
                    vim \
                    sudo \
                    git && \
    apt-get clean && rm -rf /var/lib/apt/list/*

# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
RUN if ! id $DOCKER_USER; then useradd -l -u 22222 -md /home/$DOCKER_USER \
        -s /bin/bash -p $DOCKER_USER $DOCKER_USER; fi
RUN usermod -aG sudo $DOCKER_USER && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers

USER $GITPOD_USER
# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/
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

RUN sudo ls
USER root
