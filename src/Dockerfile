FROM jupyter/base-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
# Using this as the base to get user working right
ARG DOCKER_USER=jovyan
ARG ENV=src

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


# debug tools and sudo need for conda activate
USER root
RUN apt-get update && \
    apt-get install -y make \
                    vim \
                    sudo \
                    git && \
    apt-get clean && rm -rf /var/lib/apt/list/*

# need sudo
RUN usermod -aG sudo $DOCKER_USER

USER $DOCKER_USER
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
