# Restart

Restart is an open source tool for PPE forecasting. As illustrated below,
our model factors in several different sources of data in order to inform its
projections.

The aim of this project is to provide a robust and modular infrastructure for
generating PPE projections based on data that is rapidly changing and evolving.

![Conceptual](doc/conceptual.dot.jpg)

## Installation

As a Python package this project is easily available through PyPi. To install
with pip:

```bash
pip install restart
```

Note that we require Python 3.8 or greater.

## Usage

The `RestartModel` class is the main interface for generating models. The
following block of code shows how to instantiate a statewide model for the
state of Washington (using Bureau of Labor Statistics data to specify the
population).

```python3
from restart import RestartModel

restart = RestartModel(population='oes', state='Washington')
model = restart.model
```

From here, you can access data fields for various aspects of the model. For
example, you can access detailed population breakdown in a Pandas dataframe
as follows:

```python3
population = model.population.population_pP_tr.df
```

The stockpile interface is currently in the process of being greatly simplified.

For examples of this in use, see the notebooks in [restart-notebooks](https://github.com/restartus/restart-notebooks),
which demonstrate how to generate projections, override default assumptions, and
visualize data within the model.

## Data Sources

All data currently used by this package can be found in the [restart_datasets](https://github.com/restartus/restart_datasets)
package. Data being used in the forthcoming V3 release isn't publicly availble
yet, but it will be released in the coming weeks.
