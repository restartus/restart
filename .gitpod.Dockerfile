FROM restartus/src
LABEL MAINTAINER="Admin Restart<admin@restart.us>"
USER root

# To be used in gitpod.io must be debian/ubuntu or alpine based
# Must also have a gitpod use
# With the jupyter/scipy-notebook base we end up with two users
# gitpod and joyvan

### Gitpod user ###
# https://github.com/gitpod-io/workspace-images/blob/master/full/Dockerfile
# '-l': see https://docs.docker.com/develop/develop-images/dockerfile_best-practices/#user
RUN useradd -l -u 33333 -G sudo -md /home/gitpod -s /bin/bash -p gitpod gitpod \
    # passwordless sudo for users in the 'sudo' group
    && sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/gitpod
WORKDIR $HOME

### Gitpod user (2) ###
USER gitpod
# use sudo so that user does not get sudo usage info on (the first) login
RUN sudo echo "Running 'sudo' for Gitpod: success" && \
    # create .bashrc.d folder and source it in the bashrc
    mkdir /home/gitpod/.bashrc.d && \
    (echo; echo "for i in \$(ls \$HOME/.bashrc.d/*); do source \$i; done"; echo) >> /home/gitpod/.bashrc

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

## Now make sure gitpod user as the same rights as the joyvan in src/Makefile
USER gitpod
