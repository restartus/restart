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
