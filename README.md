# COVID-19 Restart the World

Getting the world up and running again isn't going to be easy. This project is a start at making that easier. Feel free to take pieces and contribute. While we wait for an effective treatment or a vaccine, we need all these pieces to save lives from the infection and get the economy back to work.

It has four major components:

1. Modeling the Need. Model the entire world of the COVID-19 response from the
   epidemeological models, to the consumer confidence model and finally to the
supply chain models that estimate how much Personal Protective Equiptment (PPE),
Test kits and other equipment is needed to make it work.
3. Providing the Material. This so confusing that having a set of templates that
   you can embed into any website to provide the latest training, the condensed
recommendation is critical. And then on the backend a marketplace that is easy
to setup so you can buy or download what you need in one step.
2. Changing Norms. No amount of equipment works without changing how people
   work, live and play. This is a set of behavioral models and content that
works against the different segments that need to be protected. From children,
to the elderly to specific groups that are disportionately effect, getting the
right message at the right time is key.
4. Community. Getting the entire network of public, private and non-profit
   organizations working together.

# Table of Contents

1. [Conceptual Diagram](#conceptual-diagram)
2. [Project Management](#project-management)
3. [Directory Layout](#directory-layout)
4. [Versions and Releases](#versions-and-releases)
    - [Release Points](#release-points)
    - [Release Notes](#release-notes)
    - [Excel Bug Notes](#excel-bug-notes)
5. [The Various Documents](#the-various-documents)
6. [Data Sources](#data-sources)
7. [Mac Installation Guidelines](#mac-installation-guidelines)
    - [Using Git LFS and XLTrail](#using-git-lfs-and-xltrail)
8. [Other Repos](#other-repos)
9. [Release Schedule](#release-schedule)
10. [GitHub, XLTrail, and Git LFS](#github-xltrail-and-git-lfs)
11. [Notes on Using Excel](#notes-on-using-excel)

# Conceptual diagram

We are building a system that calculates from several classes a system that
looks like:

![Conceptual](doc/conceptual.dot.jpg)

# Project Management

The overall project is managed with [Github
Projects](https://github.com/restartus/covid-projection/projects/1). The process
works this way:

1. We assign items to people for the weekly sprint. Check the board to see what
   issues you own
2. The syntax of each issue is in brackets Estimated time in hours to complete  Item name
   (actual used), so for instance `[3] Insert new Class (2)` which means it will
take 3 hours to complete and you've used 2.
3. When estimating times, we are using the Fibonacci series as a rough guide so
   assign hours as when estimating as `0.5, 1, 2, 3, 5, 8, 13, 21` for how many
hours something will take.
4. We don't use that for for much now but it is a good way to see how accurate
   we are. You should try to turn on your 30 minute announcment on and see how
log it takes.

# Directory Layout

The directory layout has a few major areas:

- [data](data). This is where all the raw data is kept. Right now, this uses Git
  LFS so that we have version control and this works since the data sets are
relatively small at at most a few GB. You do need git lfs installed to read
this.
- [bin](bin). This is where the developer tools live. They are mainly a subset
  ported from @richtong at https://github.com/richtong/src . The most important
is install.sh which should install the development environment for Mac (for
sure), Linux (hopefully) and Windows is in development. Our standard dev
environment is Mac, so let @richtong know if you want to become a maintainer for
the other builds.
- [lib](lib). Used by bin, this gives a standard development environment with
  some standard variables like SOURCE_DIR you can use everywhere
- [model](model). This is where the new V2 model lives
- [nb](nb). This is for experiments and is our poor man's Jupyter Hub for
  notebooks
- We do have some Excel sheets at the top, there is technical debt to fix the
  Github actions to pull data from below, but they are named files that you copy
in Athena sheets


# Versions and Releases

The main release scheme is to alternate between adding features (the v1, v3,...)
and then solving technical debt issues and solidifying things, you can think of
these a v1, v1.x, v2, v2.x, etc

Our first v1 models (codenamed Athena) are in the [excel](excel) these are
Excel spreadsheets and they have now stabilized with a series of 1.x releases.
All versions are kept there.

Our next generation or v2 models (codenamed Balsa) are the conversion to Python
and implement the Surge models once again and then will add additional
extensions. Most of this work lives in the Jupyter and src subdirectories.

Our v2.x models (codenamed Concrete) will be a technical catchup release where we
put in the CD/CI features

As with all semvar compliant systems, major versions v1, v2,... maintain the
same interface, that is they produce the same output and are called the same

## Release Points

The system release two spreadsheets right now as of v1.x at
https://github.com/restartus/covid-projection/releases. These are right taken
from the files at the root and renamed appropriately. So when you want to do

- covid-who-surge-washington.xlsx. This is the copied latest file that is the large model
  for State of Washington including SOC
- covid-who-surge-single.xlsx. This is the
  template is for a new client. It is not reentrent, so for each new client, make a copy
- covid-who-surge-single-cook.xlsx. Thsi is the first release that uses the
  single for Cook county restaurants

## Release Notes

- v1.4.5 Removes the data table from main washington model and creates a county
  only model
- v1.4.4 First cut of the stockpile model
- v1.4.2. This has fixes for disinfection calculation and introduction to a
  single sheet models
- v1.3.1. Fixes the the washington surge and has the new york city surge

## Excel Bug Notes
If you put a data table inside the system, you will get a external content
error. To fix this, you should go to the Data tab and look at connections. This
is the place to remove external connections
[External](https://answers.microsoft.com/en-us/msoffice/forum/all/excel-for-mac-external-data-connections-have-been/03d3efa9-d540-4b00-8bc8-a06ddb7c4ea1)

# The Various Documents

- [README.md](README.md) You are reading this, the basic introduction
- [INTRODUCTION.md](INTRODUCTION.md). The model and how it works at a high level
- [RESEARCH.md](RESEARCH.md). Various call reports on new ideas


# Data sources

## Apple Mobility

A regularly published CSV on mobility data
[Apple](https://www.apple.com/covid19/mobility)

## Google Mobility

A regular data source from [Google](https://www.google.com/covid19/mobility/)

## The PowerBI cube

The supporting documents needed are mainly in PowerBI.
- [OCC Based
  Employment](https://azure.microsoft.com/email/?destination=https%3A%2F%2Fapp.powerbi.com%2FMobileRedirect.html%3Faction%3DOpenReport%26reportObjectId%3De9e58394-451a-429b-aed1-20ef6e317dc4%26ctid%3D1e355c04-e0a4-42ed-8e2d-7351591f0ef1%26groupObjectId%3Df2f0cf78-3695-4dd6-a6fd-cf2063d3195c%26OpenAppFromWindowsPCAndTablet%3Dfalse%26emailSource%3DReportInvitation&p=bT0xN2RlMjVkYy04ODg4LTQwYmYtOTJmYy1iNDEwODVlNDAzZDEmdT1hZW8mbD1Nb2JpbGVSZWRpcmVjdC5odG1s)

# Mac Installation Guidelines

@richtong will shortly generate instructions for Windows machines, but here is
an outline of steps:
First you need to install [Homebrew](https://brew.sh/) so that you can automatically install the
   rest of the stuff. This is done with Terminal and you have to run a machine
incantation. Just copy and paste in the next line

```
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

Now that you have done that, then run the following commands which installs the
right pieces for you:

```
brew install git git-lfs
# You want this in a dedicated directory
mkdir -p ~/ws
```

Now you need to create a logon at [GitHub](https://github.com) and then ask
@richtong for rights to get into this repo then find a nice place for the
forecast and run these commands to get all the latest spreadsheets directly into
your machine

## Using Git LFS and XLTrail

You will need to install Git LFS as the models are quite large at 200MB and up
with and it will really clog your machine:

```
git lfs install
# to get whatever version you need, just use the version number
git checkout v1.0
# to get the latest daily developmen release
```

Also we support the use of release tags, the current versions are:
- v1.0. This version went to the State of Washington for their surge mask
  forecasting and is over at the Office of Financial Management. This contains
all the data in a single sheet and runs on Excel or Google Sheets.
- rich-dev. This is the development fork, please use with caution.

```
# assuming you put this into a directory called ws
cd ~/ws
git clone https://github.com/restartpartners/covid-forecast
# You will be asked to enter your user name and password
cd covid-forecast
# this says get big files like Excel spreadsheets
git lfs init
# pull means get the latest from the cloud
git pull
```

And that is all there is to it, rather than asking for one at a time. You can
then edit the sheets directly as often as you like.

```
# This gives you your own private copy so no one can mess with your stuff
# so if the branch can be any name but by convention it is typically your
# name and then a dash and then what you are working on
git checkout -b _matt_-_utah_
# This makes sure that the server knows about your private copy
# origin means the cloud
git push --set-upstream _matt_-_utah_ origin
# now make any changes that you want
# when you are done, you just commit the changes and then push it to the cloud
git add -A
git commit -m "I did some amazing things and other comments"
git push
# When you want others to see it, let @richtong know and he will merge it into
the base so others can see it
```
# Other repos
The best way to work on this is to see what others are doing. In
[https://github.com/restartpartners](https://github.com/restartpartners])
so here are the certain ways of doing it which are forked:

- https://github.com/NYTimes/covide-19-data. This is the New York Times data repository
- https://github.com/datasets/covid-19. Time series data from datahub.io
- https://github.com/ImperialCollegeLondon/covid19model their specfic model
- https://github.com/neherlab/covid19_scenarios The summary and visualization of
  all scenarios

# Release Schedule

## v1.4 - In concept

Add non-Washington cubes to the model. Create a separate sheet for
non-Washington that has the simplified model.

Enable:
1. Picking of different rows will be done by matching IDs rather than indexing
2. For a given class, you can select a PPE row and then give it a weight. That
3. The stretch goal. Patients will be added as a column so we can spread them
   across the cubes

## v1.3.2 - Surge model with non-Washington sheet -- In development
Uses the same basic form, but we do not assume Washington population data

## v1.3.1 - Released - Washington Surge Model Corrected, NYC and Snohomish model -- in Validation

This is the fixed model as the transition to Excel corrupted some cells and we
lost formulas.

The enhancements are:

1. AT the end of the model, any pivot table can be inserted into the model and
   it will calculate based on that. It also slices a county appropriately based
on the Washington Cube
2. The model now uses named ranges in Analysis 8 and 9 so just changing the
   analysis is not just changing names rather than relinking absolute cell
references
3. Adds the NYC analysis as well at the bottom as well as Snohomish county and
   it now uses a Pivottable and external data rather than copying it all into
the sheet, so this becomes more of analysiss tool.
4. Also adds a checksum in Analysis 8 and on to make sure the additions are
   corect. Note that if you put in a Level but not an Essential, you will have
issues. That is if no Essential is listed, it is not added to the total. That's
an easy way to exclude groups by the way.
4. This is on the way to genericization so if you want to change and to add new
   analysis, copy down the latest Analysis and then change the formulas in the
SUMIFS after you define new range names, the range names are where you replace
the `N`with the number of the analysis

AnalysisNItems. All the items being managed
AnalysisNLevels. The protection levels. These are numeric and index off the
protection level table. Soon they will be a tuple. The levels can be a fraction
in which case it takes a percentage from the next level, so 4.2 means 20% from
level 5 and the rest from level 4
AnalysisNEssential. The degree of urgency to start. Arbitrarily, less than 4
means a non-essential, (aka a non-bootstrap of the economy worker)
AnalysisNLowLower. The lower bound of non-essential, >0
AnalysisNLowUpper. The upper bound, usually <4
AnalysisNHighLower. The lower bound of essentially, usually >=4
AnalysisNHighUpper. The upper bound, usually <=999

To change a pivot, make sure you have lots of rows below, more than what the new
pivot needs, the go to Pivot Analysis/Change Data Source.

Right now these are absolute paths, this still needs to get resolved how to make
this portable.

Then you have to relink all of the data out of the pivot table. This takes some
time as you can't just copy and paste, but have to do a hard equal to get the
right extraction

The Pivot Table does not work with Hierarchical data, so in that case it is
probably better to either go to the owrk of chaning the lables so they are or to
just copy the table in.

## v1.0 - Released - Washington State Surge Model (deprecated)
This is the model that went to the Washington State Office of Financial Management and we will send updates as needed. It has the following features (or bugs depending on how you look at it). Note that this model has a big bug, the formulas were inadvertently deleted, so use 1.3.1 or later

- Washington State only. No splits nor is this a country model
- Five forecasts in one. NAICS-2, NAICS-6, SOC, Small Business only, Not employed splits
- Depends on WHO EFST v1.2 surge to estimate healthcare needs augmented with DOH Tier 1-4 dates 14 April (not updated to latest) and some LNI rules for Construction but not updated to latest phases
- Estimates conserved use

# Github, XLTrail, and Git LFS

Github and Excel spreadsheets are not really used much together, but as we are
going to have both Excel spreadsheets and real code integrated, this seems like
a good place to put it.

There are a few changes to your workflow when you are using this tool that is
different from just storing Excel on your machine and emailing models around or
having it in a shared dropbox:

1. The versions are taken care of for you. This repo uses [XL
   Trail](https://xltrail.com) to monitor all the spreadsheet changes. It
generates a cell-by-cell comparison of what's actually changed.
2. Github keeps track of every revision, so you can have a different set of
   models and these get tagged so you can make sure you are getting the right
model. This is independent of the filename of the model, so you can make sure
you are getting the right model at the right time.
3. It stores every copy of the model in it so you can always roll back and
   recover a model that is way cool..
4. The final piece is Git LFS or Large File Storage, this makes it blazingly
   fast to store even GB models (we do!) into the system

# Notes on using Excel

## Dealing with PivotTables

Here is are the difficult parts on a Mac. A Pivot table cannot be moved with
copy and paste, instead, you need to go to the Ribbon and view analyze and there
is an entry called `Move Pivottable` which lets you move it.

When you select into a Pivot Table, you get a reference that is a cell number,
you get a named reference that looks like `PIVOTTABLE`. This works really well
for anything that is developed that has the same number of rows which is great.


## Excel does not like Google Sheets

There is some sort of bug where Excel does not like certain forumulas in Google
Sheets so it deleted all the formulas that were using the Sumproduct. So this
formula needed to be recreated on the Excel side and we should not use Google
Sheets as a result.

## The resource formula

The key formula in the spreadsheet is the that takes the level of protection and
multiplies it against the row that is at the PPE level

The first formula only handled discrete rows like, so it indexes against a fixed
protection at G7:Q13 and then indexes into it with the D365 which is the
protection level. We add one because we index at 0. Then we calculate what the
column. Then multiply by the population

```
=@INDEX($G$7:$Q$13,$D365+1,COLUMN(H365)-COLUMN($G343)+1)*$E365
```

## Handling blending of rows
In many cases, a particular industry or job classification does not fit into any
one category, so we use sumproduct to figure this out. The key is to find the
region and then spread the data

So this first calculation gives you the two rows

```
=sumproduct(_two columns in the use matrix_, _the percentage split between the
two_)
```

The way that you collect the sum is by using the trick that modulo 1 gives you a
fraction so mod(3.4, 1) is 0.4 :

This is where the spreadsheet broke because Google Sheets and Excel,

```
{MOD(protection,1),
```

Now this gives the weight average use and then you just multiply by the
population and you are done


```
= sumproduct * population
```

One problem with
[Sumproduct](https://blog.udemy.com/excel-sumproduct/?utm_source=adwords&utm_medium=udemyads&utm_campaign=DSA_Catchall_la.EN_cc.US&utm_content=deal4584&utm_term=_._ag_95911180068_._ad_436653296108_._kw__._de_c_._dm__._pl__._ti_dsa-841699839063_._li_1027744_._pd__._&matchtype=b&gclid=EAIaIQobChMI-Leli9jD6QIV9Al9Ch3BXgn-EAAYASAAEgLSJfD_BwE) is that it does not like the vectors to be of
different shapes, so you can't do `sumproduct({1, 0}, {1 ; 0}), it needs both to
be row vectors.

In another note when used with a
[Boolean](https://exceljet.net/excel-functions/excel-sumproduct-function), you
can use it if you do a double negative to coerce TRUE/FALSE into a number
```
sumproduct( --(A2:A6="TX"), B2+B6)
```
will only add numbers where the A column has the string "TX" in it. So you need to
[transpose](https://support.office.com/en-us/article/transpose-function-ed039415-ed8a-4a81-93e9-4b6dfac76027) them first.

So the key formula looks like this where $J$7:$T$13 is the table and $D51 is the
index into it. Note that it automatically rounds down. Then the column
calculation makes sure you get the correct column starting from J, finally you
want the row below and then the trick is to transpose the next values.

This gets rid of the need to use the parentheses notation which might not be
that portable. This is just a simple function now. were E51 has 1-mod(d51) or
the amount for rounddown(e51,0) and mod(d51) is the fraction above.

```
=SUMPRODUCT(OFFSET($J$7:$T$13,$D51,COLUMN(J:J)-COLUMN($J:$J),2,1),TRANSPOSE($E51:$F51))*$G51
```

## Guards on the SUMIFS
The next complicated formula relies on ranges and does the summing. The main
trick here is that it uses SUMIFS as a conditional and you need to have a
protection level one greater at the end of each, so there is a mythical "7" or
N+1. It made construction of the model very neat as a result.

## Automatically deployment

[xltrail](https://www.xltrail.com/blog/how-to-manage-and-release-excel-files-on-github-part2)
has a great explanation of how to make this work but see .github/workflow for
additional files.

The main trick here is the need to add a step to checkout the right Excel
spreadsheet.

To make the deployment work, there is a named file, currently
covid-surge-who.xlsx which you need to copy the latest model into. Do not
symlink this as git lfs will get confused on the build

## Automated Testing
You can use [XLWings](https://docs.xlwings.org/en/stable/installation.html) to
run an Excel application from Mac or PC. This uses a PIP package to control
Excel.

Since GitHub Actions allows runneers with Windows, you could theoretically start
a Windows machine, load Excel and run it with the Python to do testing. Man that
seems complicated though.

Another approach might be to take models which are compatible with Google Sheets
and push the model into Google Drive and drive it with Javascript

## Mobility Modeling

We need a way to model economic behavior and mobility.
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
