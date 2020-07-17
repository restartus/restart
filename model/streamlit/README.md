# Streamlit and building a graphical application

[Streamlit](https://link.medium.com/AtvAhw3Mh7) is a new library that is way
easier than Flask for creating applications.

The complete stack looks like:

1. Python PIP modules for integration into existing systems
2. Streamlit for display which you can easily get running with Docker and Google
   App Engine
3. For backend modules, do a REST api with Flask to create a nice service

## Demo application

### [stock.py](https://link.medium.com/AtvAhw3Mh7)
A stock demonstration that pulls from Yahoo and you should see running on your
local machine

```
streamlit run stock.py
```

### [car detection](https://link.medium.com/KWw8FN7Qh7)
This shows how to build for Heroku. But the cool thing is that it shows. Note
that you don't want to check in the weights that are automagically downloaded

```
streamlit run cars.py
```


## Other demonstrations straight from github

```
pip install streamlit opencv-python
# YOLO Detection
streamlit run https://raw.githubusercontent.com/streamlit/demo-self-driving/master/app.py
# Uber pickup
streamlit run https://raw.githubusercontent.com/streamlit/demo-uber-nyc-pickups/master/app.py
```

## Installation

Run `make install` in this directory

## Installatino of Google Accounts (not done yet)

This is probably the trickiest part, but the general scheme for all GCloud is:

0. This uses the include.sh scheme or @richtong and @sammck where there is a
   standard workspace called by convention [~/ws/git/src](~/ws/src) for the
organization and each project lives in an [~/ws/git/src/extern] section where
you can operate. This gives you a common development environment and variable
set.
1. Have a Billing Account (setup once for the entire project) and kept in
   [Lobster1234](https://lobster1234.github.io/2017/05/14/get-started-on-google-cloud-with-cli/)
has gist on this that is slightly old, for instance the Billing is now a `beta`
feature and not an `alpha`. For this project we have a single billing system.
The setup of billing is in [ws/git/src/bin/gcloud-init-organization]. This sets
some global variables you can get after running [ws/git/src/bin/install.sh] to
get the environment specifically WS_GCP_ORG
2. Then for each project there is a separate project space for it that is set
   for each repo that contains the project. Right now for simplicity, we have
one "big repo" that has several submodules in [extern](ws/git/src/extern) and
you give it a production system and a staging system with WS_GCP_PROJ_PROD
and WS_GCP_PROJ_STAGE
[glcoud-init-project.sh]
2. Have a dev project for each developer (so this is setup once per developer
   and kept in WS_DEV_GCLOUD which you start with, so when you joing, there is
[glcloud-init-dev.sh]
[ws/git/src/bin/gcloud-init-dev.sh] which is WS_GCP and where you normally push
