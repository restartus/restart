FROM restartus/src:latest
# Set environment for setup

# To be used in gitpod.io must be debian/ubuntu or alpine based
# Must also have a gitpod use
# With the jupyter/scipy-notebook base we end up with two users
# gitpod and joyvan
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


# set_env(user,conda-env)





LABEL MAINTAINER="Admin Restart<admin@restart.us>"



# Ubuntu debug for docker containers (use with m4)
USER root
RUN mkdir -p /var/lib/apt/lists && apt-get update && \
    apt-get install -y make \
                    vim \
                    sudo \
                    gosu \
                    git && \
    apt-get clean && rm -rf /var/lib/apt/list/*

# src specific for Docker
# https://pythonspeed.com/articles/activate-conda-dockerfile/




# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/



# create the environment for the joyvan user which is used for notebooks
# note that conda does an init here but it is for the joyvan identity
RUN conda create --name nb && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name nb --quiet --yes \
                voila \
                confuse \
                ipysheet \
                bqplot \
                ipyvuetify \
                voila-reveal \
                voila-vuetify \
                h5py \
                && \
    conda run -n nb pip install \
                restart \
                tables \
                && \
    conda clean -afy && \
    conda init


# this creation is required for gitpod so we have the right gitpod
# https://github.com/gitpod-io/workspace-images/blob/master/full/Dockerfile
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
USER root
RUN groupadd -g 33333 gitpod

USER root

# adapted from
# https://github.com/restartus/gitpod/blob/master/components/image-builder/workspace-image-layer/gitpod-layer/debian/gitpod/layer.sh
# users in the 'sudo' group for non gitpod entires, gitpod does not
# allow sudo so this is for other dockerfile RUN getent group gitpod || addgroup --gid 33333 gitpod
RUN useradd --no-log-init --create-home --home  /home/gitpod --shell /bin/bash \
            --uid 33333 --gid 33333 gitpod && \
    usermod -aG sudo gitpod && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/gitpod
WORKDIR $HOME

# all the conda files owned by jupyter:users so add to the group
USER root
RUN usermod -aG users gitpod && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER gitpod

# which will use the source package

# conda init does not work in a bash script so set it here
# https://stackoverflow.com/questions/55507519/python-activate-conda-env-through-shell-script
#
     # source "$HOME/.bashrc" && \  # does not work
USER gitpod
RUN echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "finished"

USER gitpod
RUN conda env list
RUN echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate restart" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate restart

