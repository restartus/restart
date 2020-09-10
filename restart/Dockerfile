FROM jupyter/base-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
ARG DOCKER_USER=jovyan
# We would use nb, but this notebook does not honor
# .bashrc or allow conda activate
ENV CONDA_ENV=restart


# This is set for make files of restart
#
# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/
# Call create_conda(env) to prep and finish_conda() after ## create_conda_(env, python_version,pip, pip_only)


#
# https://github.com/gitpod-io/gitpod/tree/master/components/image-builder/workspace-image-layer/gitpod-layer
#
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux





# create_user(user, group, groupuserid)


# set_env(user,conda-env)




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


# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
USER root
RUN usermod -aG sudo $DOCKER_USER && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $DOCKER_USER


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


USER $DOCKER_USER
ENV HOME=/home/$DOCKER_USER
RUN conda env list && \
    echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate $CONDA_ENV" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate $CONDA_ENV


WORKDIR /home/$DOCKER_USER/workspace
