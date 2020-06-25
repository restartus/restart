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
works with github. Which is sad

Most of the actual work is kept in a Jupyter Notebook
[README.ipynb](README.ipynb) points to the latest one. You can launch from
https://colab.research.google.com to view it or you can see it statically
rendered on https://github.com

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

![Alt text](https://g.gravizo.com/source/custom_mark1?https%3A%2F%2Fraw.githubusercontent.com%2Frestartus%2Fcovid-projection%2Frich-demo%2Fmodel%2FREADME.md)
<details>
<summary></summary>
custom_mark1
  digraph G {
    size ="4,4";
    main [shape=box];
    main -> parse [weight=8];
    parse -> execute;
    main -> init [style=dotted];
    main -> cleanup;
    execute -> { make_string; printf};
    init -> make_string;
    edge [color=red];
    main -> printf [style=bold,label="100 times"];
    make_string [label="make a string"];
    node [shape=box,style=filled,color=".7 .3 1.0"];
    execute -> compare;
  }
custom_mark1
</details>

![Alt text](https://g.gravizo.com/source/custom_mark10?https%3A%2F%2Fraw.githubusercontent.com%2FTLmaK0%2Fgravizo%2Fmaster%2FREADME.md)
<details> 
<summary></summary>
custom_mark10
  digraph G {
    size ="4,4";
    main [shape=box];
    main -> parse [weight=8];
    parse -> execute;
    main -> init [style=dotted];
    main -> cleanup;
    execute -> { make_string; printf};
    init -> make_string;
    edge [color=red];
    main -> printf [style=bold,label="100 times"];
    make_string [label="make a string"];
    node [shape=box,style=filled,color=".7 .3 1.0"];
    execute -> compare;
  }
custom_mark10
</details>

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
