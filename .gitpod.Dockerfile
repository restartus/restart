FROM restartus/src
LABEL MAINTAINER="Admin Restart<admin@restart.us>"

# To be used in gitpod.io must be debian/ubuntu or alpine based
# Must also have a gitpod use
# With the jupyter/scipy-notebook base we end up with two users
# gitpod and joyvan


# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh



# taken from $1


# src specific for Docker
# https://pythonspeed.com/articles/activate-conda-dockerfile/




# Emulate activate for the Makefiles
# https://pythonspeed.com/articles/activate-conda-dockerfile/



#create the environment for the joyvan user which is used for notebooks
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
                && \
    conda run -n nb pip install \
                tables \
                && \
    conda clean -afy && \
    conda init


# this creation is required for gitpod
# https://github.com/gitpod-io/workspace-images/blob/master/full/Dockerfile
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
USER root
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod \
    # passwordless sudo for users in the 'sudo' group
    && sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/gitpod
WORKDIR $HOME
# Testing sudo
USER gitpod
RUN sudo ls

USER gitpod
# use sudo so that user does not get sudo usage info on (the first) login
RUN sudo echo "Running 'sudo' for Gitpod: success" && \
    # create .bashrc.d folder and source it in the bashrc
    mkdir /home/gitpod/.bashrc.d && \
    (echo; echo "for i in \$(ls \$HOME/.bashrc.d/*); do source \$i; done"; echo) >> /home/gitpod/.bashrc

# which will use the source package

USER gitpod
