# Model v2
This reimplements the surge model with simple dummy data This uses Pipenv for managing packages because conda didn't install correctly an does not deal with streamlit properly. Eventually we will move this to a docker container. Here are the basic things we are doing:

1. A decision workbench so that in one click you can get every data source and
   code base in the world on your desktop.
2. A set of layers for gathering data sources
3. A set of new data sources that uses these layers
4. A core model that integrates all of this into something

The main goal is to:

1. For developers provide a one click stop to load *every* data source and
   *every* code base for COVID-19 pandemics
2. For decision support staff, that is the Excel model builders who are
   preparing these analyses to help people.
3. For business decision-makers, it's the way that they can count on making
   decisions with the best decisions available.

## The model structure over view in a nutshell
In a nutshell, to create any model, you just create a chain with parameters by
taking a look at [main.py](main.py) as a template but you can with a one liner
run the entire model. See [doc](doc) for the parameters and model

```python
# instantiate any model this way, set parameters as needed
# document lives in ./doc
model = Model(name)
  .configure(LoadYAML("california"))
  .set_population()
  .set_resource()
  .set_consumption()
  .set_economy()
  .set_disease()
  .set_behavioral()
# to interactively display and change the model
Dashboard(model)
```
There are host of parameters for each and many options, but this let's you
create as many models as you want.

## The Maintainers

If you have questions about the model, the you can contact:

@richtong - most other others
@lucathahn - [load](load) and [pop](pop)

## Code structure and documentation

The main model elements and listed and see [doc](doc) for the documentation
pulled from Docstrings, you should follow the Docstrings recommendation. If you
want to see any particular entry, the look there for the html file:

1. The main directory has the main modules and classes
2. Then each subdirectory has a subclasses.
3. [Load](loader). These are the low level classes that handle basic reading.
   The first two are load_yaml and load_csv that know how to bring raw data into
   dataframes.
1. [Pop](Pop). Population modules. These know how to load different datasets.
   The test one is done in YAML. The real OES data is there as well but is not
   yet filtered

# Building your development environment

If you are editing with an editor like vim which uses the external python
environment for checking, make sure you run `pipenv shell` so that you get the
correct version of python and pipenv

## Installation

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
And you may have to fix `PipFile` and bump the version to 3.8 as we depend on
3.8 features


## A note for VI users

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

## Running with Pipenv (Recommended)

Right now there is some sort of bug in conda that keeps it from installing, so
this is deprecated. Also streamlit is not yet supported by Conda, so that's
another deterrent so to get this running:

```
brew install pipenv
# to see the help on the various comamnds
make
# to create the environment, make sure homebrew is loaded
make pipenv
# As you debug, you should run make lint
make lint
# run this to just get command line output
make main
# to run with the debugger
make pdb
# to run the visual interface
make web
````

## Running in a Docker container (Will eventually be used for deployment)

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
# Writing code: Logging, static testing and runtime and streamlit

## Running with streamlit



## Logging

We define logging somewhat magically by using the same variable name and this
links all the logging together [Stackoverflow](https://stackoverflow.com/questions/40495083/using-python-logging-from-multiple-modules-with-writing-to-a-file-and-rotatingfi)
We use a utility to handle this which correctly deals with the root logger that
uses the same name as the model. Then each class has a logger with it's own
identifier to make it easy to create logs.

We do not use module logging although this is available. We use our own
opinionated logging tool that dumps logs hierarchically into `main.log`. Each
module you create should have this in the class __init__() where you should see
a `log_root` coming in from the main caller. The logging code needs to
abstracted, but basically if you utter this, then log.debug will just work in
your classes and you want to pass log_root to each class:

```
        from util import Log
          def YourClass(...., log_root: Optional[Log])
            # create a sublogger if a root exists in the model
            self.log_root = log_root  # log_root is passed
            if log_root is not None:
              # create a specific logger that inherits from our log tree
              log = log_root.log_class(self)
            else:
              # just use a standalong logger
              log = logging.getLogger(__name__)
        self.log = log
        # demonstration
        log.debug(f"{log=}")  # will appear log file typically test.log
        log.critical("panic stop")   # will appear on the console
        # to change the logging levels in your code
        # to turn up the console logging and then down again
        log_root.con.setLevel(logging.DEBUG)
        log_root.con.setLevel(logging.WARNING)
        # to turn off some of the log file just
        log_root.fh.setLevel(logging.WARNING)
        # to get rid of all logging entirely works for all
        # handlers
        log_root.log.setLevel(logging.CRITICAL)
        # to add your own custom handler
        log_root.log.add_handler(_your_handler_)

        self.log_root.con.setLevel(logging.CRITICAL)
        my_test_function_that_does_not_work()
        self.log_root.con.setLevel(logging.DEBUG)
```

All logging goes to `main.log` and if you want to see it on the console then you
just need a one liner in the __init__ module or which every method you are
debugging that looks like which turns up the logging that goes to the console or
just consult the test.log:

```
    self.model.log_root.con.setLevel(logging.DEBUG)
    self.log.debug("big error in here")
    self.model.log_root.con.setLevel(logging.WARNING)
    ```

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

We use some standard tools and these are embedded into `make lint`:

2. [black](https://flake8.pycqa.org/en/latest/manpage.html). This is opinionated reformatting. It complies with pycodestyle
so if you run this with `make black` you won't get errors. We run this with line
length of 79.

Then with `make test` you will get these tests and if you use `install-vim.sh`
you will get them as real-time checks in vi.

2. mypy. This does static type checking
3. [flake8](https://flake8.pycqa.org/en/latest/manpage.html). This includes pyflakes, pycodestyle and mccabe
1. [bandit](https://pypi.org/project/bandit/). This is for security testing

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


# Testing (In development)
We will implement pytest, flake8 and a security add-on black

## Unit test

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


## Multitasking with tox

If you install tox then you can have multiple runners which will be faster.


# Passive test tools: Linting

These are really easy to add as part of a github actions, they are and to a
CD/CI pipeline. But first some notes on linting

[Real Python](https://realpython.com/python-code-quality/) explains the
differences
  - PEP 8 are the coding conventions
  - PEP 257 covers docstrings (which can then generate document with pydocs)

The main linters are
  - Flake8 -  Includes pyflakes, pycodestyle, Mccabe
  - Pylama - Include pycodestytle, pydocstyle, PyFlakes, Mccabe, Pylint, Radon,
    gslint
  - MyPy - Adds static typing checking
  - Bandit - check for common security issues
  - Mccabe - calculates code complexity
  - Black - Reformatter

In vim if you are using this [Syntastic](https://github.com/vim-syntastic/syntastic) then
you can use a bunch of different
[linters](https://github.com/vim-syntastic/syntastic/tree/master/syntax_checkers/python)
at development time.
  - bandit - security check
  - flake8  - See above
  - frosted -
  - mypy -
  - pep257 -
  - pep8 -
  - prospector -
  - py3kwarn -
  - pycodestyle -
  - pydocstyle -
  - pyflakes -
  - pylama -
  - pylint -
  - python -

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

## Security Testing
There is another passive utility called bandit that looks for security issues

```
pipenv install --dev bandit
bandit
```
## Pre Commit testing
The second layer of testing are pre commit hooks that run before you push. If
you run `make lint` you should pass these easily, but this is another level of
checking. [LJ Miranda](https://ljvmiranda921.github.io/notebook/2018/06/21/precommits-using-black-and-flake8/) has a good overview of how to use black and flake8

The easiest way to install is `make pre-commit` but this creates a
pre-commit-config.yaml and then runs `pre-commit install`. If you want to roll
your own, you can generate a sample with `pre-commit sample`

They use a series of github repos and then id tags to select the hooks you want
https://github.com/pre-commit/pre-commit-hooks is their standard one with common
checks.

Note the syntax for arguments is a little convoluted
[advanced](https://pre-commit.com/#advanced) but you need to add another
dictionary

```
- id: yaml
  args: [ --multiple-documents ]
```

## Github Actions for CD/CI (@lucasthahn)

Not done yet, but [GitHub](https://help.github.com/en/actions/language-and-framework-guides/using-python-with-github-actions) explains what to do  but basically you need to install and then make sure to cd
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

## Dealing with configurations

We started by using just the yaml library, but [Hackers and
Slackers](https://realpython.com/python-pathlib/) gives us a host of options.
Here's an analysis:

1. INI files. Probably don't want to use anymore, but it can be handled by
   configparser.
2. TOML files. More powerful INI files, use with the toml library
3. YAML files. The current stat of the art. You can parse with the yaml library,
   but they recommend `import confuse` instead particularly because it allows a
   direct import into argparser

This would remove alot of config that is buried in current main with the
complication that
[documentation](https://confuse.readthedocs.io/en/latest/#search-paths) explains
that you hav to sett APPNAMEDIR externally to use local files so this has to be
set outside of the system in .env for example. Note we also store the MYPI paths
here as well. This is non-standard but works for pipenv. Normally .env is only
for non-cached secrets

```
config = confuse.Configuration('model', __name__)
parser = argparse.ArgumentParser()
args = parser.parse_args()
config.set_args(args)
```
