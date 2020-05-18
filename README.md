# COVID-19 Restart the World

Getting the world up and running again isn't going to be easy. This project is a start at making that easier. Feel free to take pieces and contribute. While we wait for an effective treatment or a vaccine, we need all these pieces to save lives from the infection and get the economy back to work.

It has three major components:

1. Modeling the Need. Model the entire world of the COVID-19 response from the epidemeological models, to the consumer confidence model and finally to the supply chain models that estimate how much Personal Protective Equiptment (PPE), Test kits and other equipment is needed to make it work.
2. Changing Norms. No amount of equipment works without changing how people work, live and play. This is a set of behavioral models and content that works against the different segments that need to be protected. From children, to the elderly to specific groups that are disportionately effect, getting the right message at the right time is key.
3. Providing the Material. This so confusing that having a set of templates that you can embed into any website to provide the latest training, the condensed recommendation is critical. And then on the backend a marketplace that is easy to setup so you can buy or download what you need in one step.

## Release Schedule

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
