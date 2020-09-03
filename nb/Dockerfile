FROM jupyter/scipy-notebook
LABEL maintainer="Restart Us <admin@restart.us>"
ARG DOCKER_USER=jovyan
ARG ENV=nb



# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh



# taken from $1



# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/



# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
USER root
RUN usermod -aG sudo $DOCKER_USER && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $DOCKER_USER
RUN sudo ls


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
                && \
    conda run -n $ENV pip install \
                tables \
                && \
    conda clean -afy && \
    conda init


WORKDIR /home/jovyan/ws/restart
