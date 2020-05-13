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
2. 
3. WHO-efst

