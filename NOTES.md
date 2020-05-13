## Development Notes
Note on how the model works

# The Quarterly Census of Employment and Wages
The Q1-Q3 QBEW is a 1.6GB pull and the 2018 Annual is 500MB CSV. The location
for this is a set of CSV [data
files](https://www.bls.gov/cew/downloadable-data-files.htm) with the data
[layout](https://data.bls.gov/cew/doc/layouts/csv_quarterly_layout.htm)

area-fip


area_fips.
[FIPS](https://en.wikipedia.org/wiki/Federal_Information_Processing_Standard_state_code)
is a code used to determine what area you are looking at The codes are 2-digit
for the state. And there are county codes [FIPS
6-4](https://en.wikipedia.org/wiki/FIPS_county_code). The complete [taxonomy](https://www.policymap.com/2012/08/tips-on-fips-a-quick-guide-to-geographic-place-codes-part-iii/) is 2
digit state, 3 digit county, 6 digits tract and 1 digit of block. This data only
does 5 digits work [QCEW Aread Codes and
Titles](https://data.bls.gov/cew/doc/titles/area/area_titles.htm) but it
includes US000 for total USCMS for all combined statistical areas,
-  then there are area codes with a `C` preview which are the
(microSA)[https://en.wikipedia.org/wiki/Micropolitan_statistical_area] which are
towns of between 10-50K people. And it also include MSAs which are cities like
Seattle-Tacoma-Bellevue MSA
- CS prefix means (Combined Statistical
  Area)[https://en.wikipedia.org/wiki/Combined_statistical_area] which combines
MSA with MicroSAs to form a unit. There are 172 of these, think of them as a
great metropolitan area. So for example, Seattle CSA #14 include 4.9M people in
Seattle-Tacoma-Bellevue, Olmp, Bremerton, Mt Verson, etc.

[own_code](https://data.bls.gov/cew/doc/titles/ownership/ownership_titles.htm)
0 is total, 5 is private, 3 local, 2 state, 1 federal, 8 is total government and
9 is total except for federal Note that these are overlapping so don't sum thme

[industry_code](https://data.bls.gov/cew/doc/titles/industry/industry_titles.htm) these are NAICS coded with six digits.
agglvl_code

## Different files

there are five major files available from the NAICS-based [data
files](https://www.bls.gov/cew/downloadable-data-files.htm):

1. County High level. This is NACIS codes down to 4 digits but is all by county,
   ownership and industry. So probably good enough for 4 digits.
2. CSVs by Area
3. CSVs by Industry
5. [CSVs by Size](https://data.bls.gov/cew/doc/layouts/csv_quarterly_layout.htm). That is by employer size, but also does this by fips, and naics
   codes
4. CSVs Single Files which is 1.2GB and includes all the data (but not the
   titles

## Occupational Employment Statistics
From the US Bureau of Labor Statistics, the Occupational Employment Statistics,
they do an annual survey by SOC code:

- The [OES codes](https://www.bls.gov/oes/current/oes_stru.htm) themselves are done as a two-digit major and then four digit minor
  codess
- They have this data Nationally, by State, MSA and non-metropolitan areas
- National industry-specific and by ownership
- All data which has everything in it and all cuts.
  (All)[https://www.bls.gov/oes/special.requests/oesm19all.zip]

## Installing ODBC Drivers to read CSV
This is a little involved but there are three steps because they are not
included with Mac Excel, so you need to load third party
[drivers](https://support.office.com/en-us/article/odbc-drivers-that-are-compatible-with-excel-for-mac-9fa6bc7f-d19e-4f7f-9be4-92e85c77d712?ui=en-US&rs=en-US&ad=US):

1. `brew install cask actual-odbc-pack` and this installs an evaluation copy
   that only returns the first three rows for testing purposes.
[Actual](http://www.actualtech.com/readme.php)
2. You have to go to a utility called ODBC Manager in `/Applications/Utilites`
   and setup a System DSN or Dataset Name.
3. You should choose Actual database and then you fill in the friendly data name
   and point it to an actual file.

Loading this database is very slow in Mac Excel. So instead, you can use smaller
slices. Long term this can be in a fast datastore like PowerBI, but it is not
practical to run a 1.2GB database.

## Installing PowerBI modules
We have this in
[PowerBI](https://docs.microsoft.com/en-us/power-bi/collaborate-share/service-analyze-in-excel) and you can analyze this in Excel as well through their
sharing 
