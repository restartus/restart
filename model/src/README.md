# Model v2
This reimplements the surge model with simple dummy data

This uses Pipenv for managing packages because conda didn't install correctly an
does not deal with streamlit properly. Eventually we will move this to a docker
container

https://realpython.com/pipenv-guide/

# Installation

Here are the notes on installation, there are three ways to run this project.
All of these are done with the make file. To see available commands use `make
help`

## Preamble get the latest python and homebrew
We are assuming you have a Mac and it is naked so from
[Python](https://docs.python-guide.org/starting/install3/osx/) itself

```
# install homebrew as a bootstrap
ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
# install the latest python, the one shipped isn't latest enough
brew install python
# make sure you can run python so put it in the path
echo '[[ $PATH =~ /usr/local/opt/python/libexec/bin ]] || export PATH="/usr/local/opt/python/libexec/bin:$PATH"' > ~/.bash_profile
```

## Note that we actually use Python 3.8 
To get this and it is already installed with `brew install python`
To use it in this environment. If you need to use 3.8 for the awesome f-strings,
then you also need the latest flake8 and it detects the python version and
installs the right one or you will get errors like F-string errors with older
version of Flake like [E999](https://gitlab.com/pycqa/flake8/-/issues/421)

```
pipenv install --python /usr/local/opt/python@3.8/bin/python3
# Need to get the right linters
pipenv install --dev flake8 mypy bandit black
# get the latest
hash -r
```

And you may have to fix `PipFile` and bump the version to 3.8

## using it all with Vi

Make sure that you are using the local files in the pipenv, so you want to run
and edit in `pipenv shell`

## Natively (not recommended)
You can just install with the requirements.txt. But beware this can pollute your
machine with conflicts. it is the easiest way to just get going if you don't
have any other python projects on your machine. 
```
# install python package
make bare
# run it natively to run it for testing as a command line
make python
# to run it as a web app that will start a small webserver on your local machine
make web
```

## Running with Pipenv

Right now there is some sort of bug in conda that keeps it from installing, so
this is deprecated. Also streamlit is not yet supported by Conda, so that's
another deterent so to get this running:

```
brew install pipenv
make pipenv
make python
make web
```

## Running in a Docker container

The pipenv should be enough for casual use, but if you have problems with
getting it to run, then you can also run this as a docker container

```
brew install docker
# run Mac Docker and login
# This will create a docker image for you and push into docker hub
make docker
# this will run the streamlit web app in the container
# you can browse to https://locahost:8051 to see it
make docker-run
```

# Modules

This include `__init__`.py so that you can just include this a  module if you
are using to connect to other code

```python
from model import Resource, Model, Behavior, Economy, Disease, Population

your_model = Model() 
your_resource = Resource(your_model)
your_behavior = Resrouce(your_model
```

# Testing and linting
We use some standard tools:

2. [black](https://flake8.pycqa.org/en/latest/manpage.html). This is opinionated reformatting. It complies with pycodestyle 
so if you run this with `make black` you won't get errors

Then with `make test` you will get these tests and if you use `install-vim.sh`
you will get them as real-time checks in vi.

1. [bandit](https://pypi.org/project/bandit/). This is for security testing
3. [flake8](https://flake8.pycqa.org/en/latest/manpage.html). This includes
   pyflakes, pycodestyle and mccabe

# PIP package (not done)
There are two flavors here. A source distribution which is meant so that you can
easily include it on other machines.

A Wheel distribution where you are creating executable code, like `pip` itself.
It's a python program that's meant to be run not just used in development.

Not complete it `make package` which will run `setup.py` and gather up the
files, run a wheel compilation and push it all up there.

[Dzone](https://dzone.com/articles/executable-package-pip-install) guides us through
using `setuptools` to do this for a wheel distribution of executables.

[Micropyramid](https://micropyramid.com/blog/publishing-python-modules-with-pip-via-pypi/)
explains how to do this if you just want source code for inclusion in other
folks package:q


## Testing (In development)
We will implement pytest, flake8 and a security add-on black

### Unit test

The main choices here come down to `pytest` [Real
Python](https://realpython.com/python-testing/)
ays there is also unittest and nose2. It is laborious, but you basically have to
create alot of functions that are prefixed with `test` and then it runs them for
you via keyword search, so naming matters. You can have all tests for say
`resource.py` named `test/test-resource-1.py` and so forth

The main trick here is writing assertions with the built in `unittest` you have
to use their class, but with pytest,
[Guru99](https://www.guru99.com/pytest-tutorial.html)
you can use the built in assert() tools

Then you can use `pytest-cov` to make sure you are covering all branches.


### Multitasking with tox

If you install tox then you can have multiple runners which will be faster. 


### Passive test tools

These are really easy to add as part of a github actions, they are and to a
CD/CI pipeline

```
# looks in CWD for all python files
# if using pipenv
pipenv run flake8 
# otherwise if running bare metal
flake8
```

And if you want to ignore certain rules, you can create a `.flake8` configuraiton
file or put into `setup.cfg` so just as a  sample
To run it against an entire directory just run `flake8` without any options

```
[flake8]
exclude= .git,__pycache__
max-line-length = 90
```

`black` isn't passive, it reformat codes for you, so it's good if you really
want the right format observed and if you dare you can even put it into the
CD/CI pipeline:

```
# to install it only for development
# note black is prerelease only and pipenv will not install beta
# https://github.com/Microsoft/vscode-python/issues/5171
pipenv install black --dev --pre
pipenv install black --dev --skip-lock
# Pip only allows 79 characters per line
# note that is is destructive so make sure you commit first
# We are running this inside pipenv
pipenv run black -l 79 *.py
# if running baremetal
black -l 79 *.py
```

### Security Testing
There is another passive utility called bandit that looks for security issues

```
pipenv install --dev bandit
bandit
```

## Github Actions for CD/CI

Not done yet, but
[GitHub](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions)
explains what to do  but basically you need to install and then make sure to cd
down to the right directory and then run the checks. 

```
name: Python package

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    strategy:
      matrix:
        python-version: [2.7, 3.5, 3.6, 3.7, 3.8]

    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install flake8 pytest
        if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    - name: Lint with flake8
      run: |
        # stop the build if there are Python syntax errors or undefined names
        flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
        # exit-zero treats all errors as warnings. The GitHub editor is 127 chars wide
        flake8 . --count --exit-zero --max-complexity=10 --max-line-length=127 --statistics
    - name: Test with pytest
      run: |
        pytest
```

## Logging

We define logging somewhat magically by using the same variable name and this
links all the logging togehter [Stackoverflow](https://stackoverflow.com/questions/40495083/using-python-logging-from-multiple-modules-with-writing-to-a-file-and-rotatingfi)

What this does is to create a logger with a different name from `__name__` in
each

```
import logging

log = logging.getLogger(__name__)
```

Then in the main executable is where you put the real work. This works because
the hierarchy means that when a module is called, takes the parameters from the
parent which is in main.

```
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)
```

The main thing is that you should not run `logging.basicConfig` when you also
doing this `getLogger`, this causes duplicates because logging.basicConfig means
that that you create two streams

