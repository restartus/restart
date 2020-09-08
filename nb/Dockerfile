FROM jupyter/scipy-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
ARG DOCKER_USER=jovyan
ARG ENV=nb

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





# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/



# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
USER root
RUN usermod -aG sudo $DOCKER_USER && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $DOCKER_USER


RUN conda create --name $ENV && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $ENV --quiet --yes \
                voila \
                confuse \
                ipysheet \
                bqplot \
                ipyvuetify \
                voila-reveal \
                voila-vuetify \
                h5py \
                && \
    conda run -n $ENV pip install \
                restart \
                tables \
                && \
    conda clean -afy && \
    conda init


WORKDIR /home/jovyan/ws/restart
