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

# Note that conda does not work in gitpod, it can use pipenv but prefers bare
# pip
# create_conda env python_version conda_pip pip_only


# Gitpod runs bare pip3 and pyenv
# create_gitpod python_version conda_pip piponly)
# https://www.gitpod.io/docs/languages/python/
# pyenv install 3.8 does not work
# https://www.gitpod.io/docs/languages/python/


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


USER gitpod
RUN pyenv global 3.8 && \
      pip3 install pandas confuse ipysheet pyomo h5py h5py confuse voila voila-reveal voila-vuetify ipywidgets ipysheet ipympl ipyvolume ipyvuetify scipy altair qgrid bqplot tables restart jupyter-server tables


WORKDIR /home/gitpod/workspace
USER gitpod
