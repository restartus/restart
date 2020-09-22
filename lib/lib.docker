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
# create_conda env python_version conda_pip pip_only pip_dev
define(create_conda,
RUN conda env list | grep "^$1" || conda create --name $1
RUN \
    echo env=$1 python=$2 pip=$3 pip_only=$4 && \
    conda config --add channels conda-forge && \
    conda config --set channel_priority strict && \
    conda install --name $1 --quiet --yes python=$2 \
                $3 $5 && \
    conda run -n $1 pip install \
                $4 && \
    conda clean -afy && \
    conda init
)

#
# create_gitpod(python_version,conda_pip,pip-only,pip-dev)
# Gitpod runs bare pip3 and pyenv
# https://www.gitpod.io/docs/languages/python/
# pyenv install 3.8 does not work but 3.8.5 does, need three digits
# Not 3.8 installed only have 3.8.x and need to specificy a final versino
#  RUN pyenv global $1 && \
# https://www.gitpod.io/docs/languages/python/
# do for both bare and for ENV=pipenv
# note that ENV variables are not passed with gitpod
# Also balck in pipenv --dev needs --pre
define(create_gitpod,
    RUN pyenv global $1 && \
        pip3 install $2 $3 $4
)

define(create_gitpod_pipenv,
    RUN pyenv global $1 && \
        pipenv install $2 $3 && \
        pipenv install --dev --pre $4
)

# https://github.com/gitpod-io/gitpod/tree/master/components/image-builder/workspace-image-layer/gitpod-layer
#
# https://github.com/jupyter/docker-stacks/blob/master/base-notebook/start.sh
# https://linuxconfig.org/configure-sudo-without-password-on-ubuntu-20-04-focal-fossa-linux

define(add_group,
USER root
RUN usermod -aG $1 $2 && echo "%sudo ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers
# Testing sudo
USER $2
)

define(create_group,
USER root
RUN groupadd -g $2 $1
)

# create_user(user, group, groupuserid)
define(create_user,
USER root

# adapted from
# https://github.com/restartus/gitpod/blob/master/components/image-builder/workspace-image-layer/gitpod-layer/debian/gitpod/layer.sh
# users in the 'sudo' group for non gitpod entires, gitpod does not
# allow sudo so this is for other dockerfile RUN getent group $2 || addgroup --gid $3 $2
RUN useradd --no-log-init --create-home --home  /home/$1 --shell /bin/bash \
            --uid $3 --gid $3 $1 && \
    usermod -aG sudo $1 && \
    sed -i.bkp -e 's/%sudo\s\+ALL=(ALL\(:ALL\)\?)\s\+ALL/%sudo ALL=NOPASSWD:ALL/g' /etc/sudoers
ENV HOME=/home/$1
WORKDIR $HOME
)

# set_env(user,conda-env)
define(set_env,
USER $1
ENV HOME=/home/$1
RUN conda env list && \
    echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate $2" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    conda activate $2
)

define(set_env_test,
USER $1
ENV HOME=/home/$1
RUN echo "export ENV=conda" >> "$HOME/.bashrc" && \
    conda init && \
    echo "conda activate $2" >> "$HOME/.bashrc" && \
    eval "$(command conda 'shell.bash' 'hook' 2>/dev/null)" && \
    echo "finished"
)
