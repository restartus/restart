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

## A note on using Latex

This file lives in README.tex.md and (Texify)[https://github.com/apps/texify] is
a Github application that automatically renders README.md with Latex formulas
which you add by putting the Latex between double dollar signs.

<p align="center"><img src="/src/tex/ce64ef4363eed7196ffc6ed3c4761042.svg?invert_in_darkmode&sanitize=true" align=middle width=9.61479915pt height=14.611878599999999pt/></p> LaTEX and it is not and this is more formally known as
and there are arbitrarily summarizations from <p align="center"><img src="/src/tex/afa921d8065c9b75169abacf1ebafddf.svg?invert_in_darkmode&sanitize=true" align=middle width=14.8230951pt height=14.611878599999999pt/></p> to the more
summarized as the nth summarization is <p align="center"><img src="/src/tex/ccfb8e56fa0de96aaf2384824f7ce8ee.svg?invert_in_darkmode&sanitize=true" align=middle width=16.3965714pt height=14.611878599999999pt/></p> in python we use the
notation <p align="center"><img src="/src/tex/9671989d0ae023df99422a88c302a0a4.svg?invert_in_darkmode&sanitize=true" align=middle width=63.899361899999995pt height=14.611878599999999pt/></p> and <p align="center"><img src="/src/tex/12e5f573a7052c63116931fd4ffb9062.svg?invert_in_darkmode&sanitize=true" align=middle width=77.3268672pt height=14.611878599999999pt/></p>

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

[Hynek Schlawack](https://hynek.me/talks/python-foss/) is our inspiration for
our development tooling. The things left to do as of July 24 are:

1. Prettier for formatting non-Python documents
2. Definitely not going to Sphinx and using Github Actions not Travis CI
3. Publish packages to PyPl from Github Actions

## Installation

Here are the notes on installation, there are three ways to run this project.
All of these are done with the make file. To see available commands use `make
help`

## Preamble get the latest python and homebrew
We are assuming you have a Mac and it is naked so from
[Python](https://docs.python-guide.org/starting/install3/osx/) itself
```
# install homebrew as a bootstrap
ruby -e "<img src="/src/tex/f1550fa5f2cbf10ea3db3f744456de91.svg?invert_in_darkmode&sanitize=true" align=middle width=1537.0778642999999pt height=24.7161288pt/>PATH =~ /usr/local/opt/python/libexec/bin ]] || export PATH="/usr/local/opt/python/libexec/bin:<img src="/src/tex/c5119ae286a706d4518cf2bd0e46f3f3.svg?invert_in_darkmode&sanitize=true" align=middle width=3388.0543884pt height=5364.0913095pt/>{{ matrix.python-version }}
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
