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
ARG CONDA_ENV=nb
ARG DOCKER_USER=gitpod

# To be used in gitpod.io must be debian/ubuntu or alpine based
# Must also have a gitpod use
# With the jupyter/scipy-notebook base we end up with two users
# gitpod and joyvan
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
COPY --chown=$DOCKER_USER:$DOCKER_USER --from=continuum /opt/conda /opt/conda
ENV PATH /opt/conda/bin:$PATH
RUN mkdir -p /opt/restart/bin
COPY --chown=$DOCKER_USER:$DOCKER_USER --from=restart /usr/bin/make /opt/restart/bin
COPY --chown=$DOCKER_USER:$DOCKER_USER --from=restart /usr/bin/vi /opt/restart/bin
COPY --chown=$DOCKER_USER:$DOCKER_USER --from=restart /usr/sbin/gosu /opt/restart/bin

# https://hub.docker.com/r/conda/miniconda3/dockerfile
# as of September 2020 note there is typo corrected
# in the Dockerfile it puts it in /usr/local but the path is /opt/conda
# we use /opt/conda to make it easy to copy out assets
# try to get running as root first
# If this works then can try
# FROM:conda/miniconda3 AS conda
# COPY --from=conda /opt/conda /opt/conda
# ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
# ENV PATH /opt/conda/bin:$PATH
# RUN apt-get -qq update && apt-get -qq -y install curl bzip2 \
    #     && curl -sSL https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -o /tmp/miniconda.sh \
    #  && bash /tmp/miniconda.sh -bfp /opt/conda \
    #     && rm -rf /tmp/miniconda.sh \
    # && conda install -y python=3 \
    # && conda update conda \
    #& & apt-get -qq -y remove curl bzip2 \
    #&&& apt-get -qq -y autoremove \
    #&& apt-get autoclean \
    #&& rm -rf /var/lib/apt/lists/* /var/log/dpkg.log \
    #&& conda clean --all --yes


# adjust permissions as root
#.RUN mkdir -p /opt && \
    #    chown -R $DOCKER_USER /opt && \
    #mkdir -p /etc/profile.d && \
    # chown "$DOCKER_USER" /etc/profile.d
USER $DOCKER_USER
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



USER $DOCKER_USER
ENV HOME=/home/$DOCKER_USER
RUN conda env list && \
    echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate $CONDA_ENV" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate $CONDA_ENV


WORKDIR /home/$DOCKER_USER/workspace

USER root
