# Excel models 1.x

This has the Excel models used with version 1.x

# Location of core PowerBI sheet

We are using a core PowerBI sheet that Erin put together. It lives in a magic
URL.

https://app.powerbi.com/groups/me/reports/b49462e7-a2d7-4258-92af-387a0c810723/ReportSection?openReportSource=ReportInvitation&ctid=1e355c04-e0a4-42ed-8e2d-7351591f0ef1
```
In our model sections are:

 - Area definition data was downloaded from https://www.bls.gov/oes/2017/may/msa_def.htm#5300004,
 - WA county population was downloaded from https://www.census.gov/data/datasets/time-series/demo/popest/2010s-counties-total.html#par_textimage_739801612.
 -  The core PowerBI data is pulled from The workforce data file used in our 2 dashboards is too big to
 be sent as an attachment, and here’s the link where you can download it. https://www.bls.gov/oes/tables.htm
 -  ‘All data’ under May 2019 is the table that we are using. Get it all XLS
     download
We have two items to think about –

1. One is the adding the sub categories and seeing if we can get everything to add up
2. The other is creating a view for each of 39 counties of Washington and each of the cities in Washington

The attached spreadsheet is one way to approximate a set of county data and city data.
Here is what I’ve done so far for just Washington State:

1. Assemble a list of the counties that comprise each Metropolitan Area
a. For example, the Seattle-Bellevue-Tacoma MSA is King, Snohomish, and Pierce Counties
b. Yakima MSA is just Yakima county
2. Get a total population estimate for each of the counties
3. Get a list of all the cities over 40,000, for example, and list them in the County where the city is located
4. Get an estimate of the Total population of the City Proper
5. Subtract all the city populations from the Counties in which they reside. This leaves the county population not in a city
6. Then we use these total population percentages to allocate the labor force data in the cube.

# California DAta

https://www.cdph.ca.gov/Programs/CID/DCDC/Pages/COVID-19/COVID19CountyDataTable.aspx
has their county monitoring information

https://covid19.ca.gov
https://calcat.covid19.ca.gov/cacovidmodels/ Their forward forecast
kkkk
# Installation

When you have a version you want to push up the chain, make sure the files have
the suffix `-vX.Y,Z` and they are all the same then run if the version is
v.1.4.7

```
make release TAG=v1.4.7
```

If you want to override the default files then run and make sure you *do not*
put in the .xlsx extension, it is assumed:

```
make release FILES=newfilewithoutextension TAG=v.1.47
```


## Note on breaking bugs

The main issue with models are in the use of the `column` which in the latest
versions of Excel, called Microsoft 365 or Office 365 have a breaking bug
because a column returns an array, so `COLUMN()` is an array and you cannot use
to index into something with an OFFSET().

The fix is to collapse an the COLUMN with SUM(COLUMN()). this does not affect
Mac Excel v16 or google sheets, but the feature called a Dynamic Array causes
automatic arrays to get created when you don't need it.

The net is that you should never save a sheet with Microsoft 365, it produces
incompatible formulas when arrays are used.

We use them in a sumproduct and this is breaking.
