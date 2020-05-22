# COVID-19 Restart the World

Getting the world up and running again isn't going to be easy. This project is a start at making that easier. Feel free to take pieces and contribute. While we wait for an effective treatment or a vaccine, we need all these pieces to save lives from the infection and get the economy back to work.

It has three major components:

1. Modeling the Need. Model the entire world of the COVID-19 response from the epidemeological models, to the consumer confidence model and finally to the supply chain models that estimate how much Personal Protective Equiptment (PPE), Test kits and other equipment is needed to make it work.
2. Changing Norms. No amount of equipment works without changing how people work, live and play. This is a set of behavioral models and content that works against the different segments that need to be protected. From children, to the elderly to specific groups that are disportionately effect, getting the right message at the right time is key.
3. Providing the Material. This so confusing that having a set of templates that you can embed into any website to provide the latest training, the condensed recommendation is critical. And then on the backend a marketplace that is easy to setup so you can buy or download what you need in one step.

## Release Schedule

# v1.4 - In concept

Add non-Washington cubes to the model. Create a separate sheet for
non-Washington that has the simplified model.

Enable:
1. Picking of different rows will be done by matching IDs rather than indexing
2. For a given class, you can select a PPE row and then give it a weight. That 
3. The stretch goal. Patients will be added as a column so we can spread them
   across the cubes

# v1.3.2 - Surge model with non-Washington sheet
Uses the same basic form, but we do not assume Washington population data

# v1.3.1 - Released - Washington Surge Model Corrected

This is the fixed model as the transition to Excel corrupted some cells and we
lost formulas.

The enhancements are:

1. AT the end of the model, any pivot table can be inserted into the model and
   it will calculate based on that. It also slices a county appropriately based
on the Washington Cube


# v1.2 - Released - Washington State Surge Model
This is the model that went to the Washington State Office of Financial Management and we will send updates as needed. It has the following features (or bugs depending on how you look at it):

- Washington State only. No splits nor is this a country model
- Five forecasts in one. NAICS-2, NAICS-6, SOC, Small Business only, Not employed splits
- Depends on WHO EFST v1.2 surge to estimate healthcare needs augmented with DOH Tier 1-4 dates 14 April (not updated to latest) and some LNI rules for Construction but not updated to latest phases
- Estimates conserved use

# v1.2.1 - Released Utah Surge Model
This model was done by Matt and its features are it is SOC based 

- SOC based
- Does splits 

# v1.1 - Target data Alpha Monday 17 May
3. Providing the Material. This so confusing that having a set of templates that you can embed into any website to provide the latest training, the condensed recommendation is critical. And then on the backend a marketplace that is easy to setup so you can buy or download what you need in one step. And finally there is a scheme for getting material to non-profits and other vulnerable folks in the population

# Why are we using Github and what is XLTrail and what is LFS
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

# How to set it all up (for the Mac)

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
# On using the repo
You will need to install Git LFS as the models are quite large at 200MB and up
with:

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

# Questions
Create an issue and we will get right to it :-)


# Development timeline
The current development timeline is:

v1.1. Add the general use of Pivottables to allow slicing the model and will
also migrate the data to an external database. This will make the model Excel
dependent. 

v2.0. Use the WHO v2 Surge model to allow Epidemiological forecasting to plug
in.

## Workspace is needed
The major thing is that you need four sheet open to run the modeling

1. Covid-surge-who-1.2.xlsx
3. WHO-efst

## Next steps
And where it goes, there are some great ideas on what to do next for the so called 1.x models

0. The v1. 2model and stability things that I’ve put in and the test of it vs pivot tables (it works!)

1. Do the 50 state model using the Hilburn model (right now called the v1.2.1 as it’s a variant of the current one)

2. Go through the PowerBi data that Mitch and Erin has done to clean up the big data cube

3. Go through the way to deliver the forecast. Mitch suggests doing low/medium/high

4. Visualization of all of this and how to make it look pretty (Bharat has some great ideas here).

5. How exactly the model works with Power BI, can we shove the model into PowerBI, if not, what’s the easiest way to put it into an XLS sheet and have it stably work

Then the really big things, the move to the v2 model

1. The move to a time series to predict the weekly consumption of PPE that is a function of economic restart and the disease progression. For economic restart, how do we model this, seems like basically a sigmoid function so maybe have a parameterized restart and each SOC has a restart time and a sigmoid start up to some limit?

2. This means integration of WHO v2 into the model and doing this automagically, The Who v2 model changes depending on inputs. That is, it projects infection and projects activity and this has to be redo regularly

3. Extensions to the model. The big one is testing requirements.

4. The addition of COVID patients specifically into the model. It is implicit right now

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

# Handling blending of rows
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
sumproduct( --(A2:A6="TX"), B2+B6) will only add numbers where the A column has
the string "TX" in it. So you need to
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

