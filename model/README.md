# Recoded Python model Studies

This takes the study done with Jupyter notebooks and turns it into code as a
demo:

## Model 0.0 feasibility of using Streamlit
This is the visual display demo using streamlit. Filled with dummy data

- [streamlit](streamlit) experiments with using Streamlit for web display.
- [model0/dashboard0.py](model0/dashboard0.py) is the spaghetti code that is the first implementation of the
  model. Retain for testing purposes

## Model that is the real python model first using streamlit as a demo v0.1

- [model0/dashboard.py[(model0/dashboard.py). This is not yet complete but
  implements the class model described in the readme
- [README.ipynb](README.ipynb). This is the main read me that describes how the
  module works. This is best read by starting https://colab.research.google.com
opening but it describes the equations and has the test code for the model.
 The main thing that it does is to make the variable names easy to understand.


## The real code for the Python model for v2.x
The other files follow the standard Python scheme and is ready for docstring
documentation
- [src](src) the source for the python. it's on the floor right now.
- [doc](doc) when we get documentation working we are using makedocs using
  docstring as the production tool.

# The main variables and constants

The most confusing part about this model are the many parameters. We use
Einstein summations and the working model is in [README.ipynb](README.ipynb)

But here are the major variables as a glossary and these usually have two forms,
the canonical dataframe and then an array form for tensors that are more than
two dimensions. In general, we operate on the array form and display with the df
form. The names change, but the first is for the surge model and the second for
the full range of data plus time series. And in colons are the class that
creates it

- Resource.res_n_df (Resource.res_na_df). Resource list main labels and it is all 1's in the surge model
  then extends to the a attributes which are mainly things like volume.
- Population.pop_p (Population_pd). The populations we are studying. In this case,
  we are talking about d details including things like number of COVID patients
in each population.
- Demand.usage_res_ln_df (Demand.usc_res_dln_df). The Usage for each protection level for a resource per capita

Then we have transformations that are typically a `to` attached:

- Population.to_usage_pl. Converts p populations to the l usage level
- Population.attr_p (Population.attr_pd). Population attributes with a 1 in the
  first column always but then you can have others like covid patients
- Population.resource_pn. Resource neede per capita
