# Recoded Python model Studies

This takes the study done with Jupyter notebooks and turns it into code as a
demo:

## Model 0.0 feasibility of using Streamlit
This is the visual display demo using streamlit. Filled with dummy data

- [streamlit](streamlit) experiments with using Streamlit for web display.
- [model0/dashboard0.py](model0/dashboard0.py) is the spaghetti code that is the first implementation of the
  model. Retain for testing purposes
- [model](model) The current v2 model
- [logging](logging). Experiments in building a robust logging system that works
  across streamlit and command line
- [altair](altair). Studies of using the Altair plotting interface to Vegas-lite
- [yaml](yaml). Experiments in using YAML as model input
- [namespace](namespace). Testing of multiple packages in the same namespace
- [iterator](iterator). Learn how to Model to iterate against all Base classes
    inside of it

## Model that is the real python model first using streamlit as a demo v0.1

- [model0/dashboard.py[(model0/dashboard.py). This is not yet complete but
  implements the class model described in the readme
- [README.ipynb](README.ipynb). This is the main read me that describes how the
  module works. This is best read by starting https://colab.research.google.com
opening but it describes the equations and has the test code for the model.
 The main thing that it does is to make the variable names easy to understand.


# The real code for the Python model for v2.x
The other files follow the standard Python scheme and is ready for docstring
documentation
- [src](src) the source for the python. it's on the floor right now.
- [doc](doc) when we get documentation working we are using makedocs using
  docstring as the production tool.

## Note we are using [gravizo.com](https://gravizo.com) to render graphs with
graphviz and test. It actually supports DOT, PlnatUML and UML Graph as well as
SVG so really useful for illustrations that are not just dumb graphics as
explained by @tlmak0 at https://github.com/tlmak0/gravizo. The way it works is
that you pass gravizo.com the URL of the README or whatever file, it will then
parse it looking for Graphviz or other commands. It works because you set a
magic tag which must be unique in the text for it to find

The main tools you need here are the raw file link which you can get by looking
at [github.com](https://help.data.world/hc/en-us/articles/115006300048-GitHub-how-to-find-the-sharable-download-URL-for-files-on-GitHub)
and clicking on the `raw` button for a file and then put it
through https://urlencoder.org to get the percent-encoding also call the URL
encode.

Although the gravizo.com site shows an easier way with a direct embed but this
[no longer](https://gist.github.com/svenevs/ce05761128e240e27883e3372ccd4ecd)
works with github. Which is sad because the only way the indirect method works
is for public repos since private repos require an authentication key.

Most of the actual work is kept in a Jupyter Notebook
[README.ipynb](README.ipynb) points to the latest one. You can launch from
https://colab.research.google.com to view it or you can see it statically
rendered on https://github.com

## Why no scientific notation

The most confusing part about this model are the many parameters. We use
Einstein summations and the working model is in [README.ipynb](README.ipynb).
Note that github markdown does not support Latex, so you have to use a
[hack](https://gist.github.com/a-rodin/fef3f543412d6e1ec5b6cf55bf197d7b) to
display it properly by using an image call, so we just remove this from this
readme, otherwise it tracks the Jupyter Notebook but without the scientific
notation.

# Class Structure

The main components of the v2 model are in a diagram

![Alt text](https://g.gravizo.com/source/custom_mark?https%3A%2F%2Fraw.githubusercontent.com%2Frestartus%2Fcovid-projection%2Frich-demo%2Fmodel%2FREADME.md)
<details>
<summary></summary>
custom_mark
  digraph "Class Model" {
    node [shape=box]
    subgraph Pop_class {
      style=filled
      P [label="Population, Essentiality"]
    }
    D [label=Disease]
    P -> D [label="Social Mobility"]
    D -> P [label=Patients]
    E [label=Economy]
    P -> E [label="Stage, Economic Activity"]
    E -> P [label="GDP, Employment"]
    subgraph Res {
      R [label=Resource]
      R -> P [label=Delivery]
      P -> R [label=Demand]
      I [label=Inventory]
      R -> I [label=Fill]
      I -> R [label=Use]
    }
    S [label=Supply]
    R -> S [label="Sales Order"]
    S -> R [label=Fulfillment]
  }
custom_mark
</details>

# The main classes
Then each major module can be subclassed from this and your can replace it. The current list of modules are and in the notation, the class name is the major part of the variable. Note that is copied from Jupyter so you will see $Latex$ formula for those of you who can read that, otherwise you can ignore it.

## Model Class 
Model or `model`. This is the core framework. It holds the dimensions and
pointers to all the module component instances. It's main use is to "dimension"
the problem so that the other subclasses know the size of the problem. It also
holds points to the entire "graph" of objects (similar to a Keras object in
machine learning. So the process is to add "layers" or model elements, then run
the model as needed with a "solver" that is used for specific purposes and later
for optimization of an objective function.

The objects in the world which has a single character $symbol$ or a 3-4
character `_short_name_` name and then some other facts

## Population Class
Population as or `pop`. This holds the population and details about it. It's
main output are two fold wtih a set of variables that are 'inside' Population

- $P_{pd}$ or `Population.attr_pd[p, d] for p Populations with d details on each such as number of covid patients or number of runs per day
- $P^R_{pn}$ or `Population.to_res_pn[p, n]`. This is a given populations use of all n resources and is the per capita, per day figure.
- $P^T_{pn}$ or `Population.total_pn[p, n]`. This is the total population usage
- $P^{LC}_{en}$ or `Population.level_cost_en[e, n]`. for every essentiality level, what is the cost for each resource n.
- $P^{LT}_{en}$ or `Population.level_total_cost_en[e, n]`. The total cost for every essential level for each resource
- $P^{D}_{ln}$ or `Population.demand_ln`. This is the conversion from essential levels to items used where l is the number of levels and n is the number of resources. It is the core burn rate analysis
- $P^{L}_{p,l}$ or `Population.to_level_pl[p, l]`. Converts a population into levels of essentiality and use
Finally there are various properties that these objects can have. these are handles as superscripts in the formula notation or as the second word in the code as snake_case.

- Burn rate $B$ or `burn` which is the use per day per person of a resource
- Total units $U$ or `total` which is the total needed for an entire population
- Cost $C$ or `cost`. The cost per unit
- Total $T$ or `total_cost`. The total for an entire population


  - Summary Level of Essentiality  `level`. The population summarized by summary
    levels
     that are used to restart the economy in phases and stop it the same way 
  - Demand $D$ or `demand`. This calculates the burn rates or usage of the
    products. In the surge model these are done per person per day which
generates an lxn matrix

## Resource class
Resource  `res`. The resources needed, it takes demand from Population and returns to the population what can actualy be supplied.

  - $R_{na}$ or `Resource.attr_na[n, a]` were Resource data for n items with a attributes (like it's volume and cost), by convention, the first column has a one in it for easy matrix multiplication
  - Supply $S$ or `supp`. The sources of supply and input of resources
  - Inventory $I$ or `inv`. What is currenty on hand

## Economy Class
Economy $E$ or `econ`. This is a model of the economy that takes in the Population and the degree of economic activity and returns the GDP and employment and other measures of work

## Disease Class
Disease $D$ or `disease`. This models the progression of the disease and takes in the population and social mobility and it returns the number of patients, deaths and recovered patients.



But here are the major variables as a glossary and these usually have two forms,
the canonical dataframe and then an array form for tensors that are more than
two dimensions. In general, we operate on the array form and display with the df
form. The names change, but the first is for the surge model and the second for
the full range of data plus time series. And in colons are the class that
creates it

- 
- Resource.attr_n_df (Resource.attr_na_df). Resource list main labels and it is all 1's in the surge model
  then extends to the a attributes which are mainly things like volume.
- Population.attr_p (Population.attr_pd_df). The populations we are studying. In this case,
  we are talking about d details including things like number of COVID patients
in each population.
- Demand.usage_res_ln_df (Demand.usc_res_dln_df). The Usage for each protection level for a resource per capita

Then we have transformations that are typically a `to` attached:

- Population.to_usage_pl. Converts p populations to the l usage level
- Population.attr_p (Population.attr_pd). Population attributes with a 1 in the
  first column always but then you can have others like covid patients
- Population.resource_pn. Resource neede per capita
