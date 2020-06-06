# Washington State specific tables

## PPE Counts per job title (@mitch, 26-May-2020)
Here is the current method for estimating labor force size for a vertical like
restaurants.  The problem is making sure all the appropriate occupational
categories for “police” or for “restaurants” are included collection of codes we
select form the BLS data cube.  Once we have completed the process by hand and
validated it, we can flag all the detailed occupational categories comprising
Police or Restaurants. I plan to teach this method to our interns and show it to
a developer so we can automate it or at least make it DIY.
 
Let’s say we get a request from the Restaurant Association of Washington State
and they want to know how much PPE they need to reopen. First, notice I picked a
geography already available in the data cube so I don’t need to assign the
Washington State numbers to sub-geographies, but note this method works fine
when we have to do that too.
 
This example is about how we make sure we get all the restaurant employees
estimated properly.  Here are the steps:
 
Go to the BLS data cube and select: State à Washington Here is the screen shot –
3.3 million in the Washing State Labor force (May 2019, BLS)

![ppe-per-job-title-image002.png]

Enter into the yellow filter box “Restaurant”
to hunt for restaurant workers or review the 23 major categories below and see
if one looks like the place to find restaurant workers. (check out 35-0000) –
but if one doesn’t pop out, use the search bo  ![ppe-per-job-title-image004.png]
 
When I type in “restaurant”  I see these occupations come up
 
![ppe-per-job-title-image008.png]

![ppe-per-job-title-image004.png]

When I click on cooks, Restaurant – the dashboard
selects 35-2014 This tells me the 35-xxxx is where the restaurant employees are
I can click on the “hosts and hostesses” and confirm 35-xxxx comes in as the
category
 
![ppe-per-job-title-image012.png]

 
Once I have done a bit of exploring it becomes clear the 35-xxxx category contains the restaurant employees, but the only labels coming up are those with “Restaurant” in them. The problem is I don’t know who I  might be missing.
 
Solution: to make sure I don’t miss anybody, I simply go select all the 35-xxxx categories, or go review the BLS detailed categories within the 35-xxxx group. Here they are:
 
![ppe-per-job-title-image014.png]
 
Now I see I hit pay dirt and have the occupations for the restaurant industry,
and I need this so we can estimate PPE needs by occupations. Hostesses and
waiters need a different volume compared to dishwashers in the back room.
 
I use the dashboard and data cube to select all the 35-xxxx occupational
categories. (I’m already in Washington State only.)
 
I hit the “clear all button” in the yellow box to remove all selections.
 
I then scroll to the 35-0000 category in the yellow box, hold down the CTRL
button and click on all the 35-xxxx categories
 
![ppe-per-job-title-image018.png]
 
Keep selecting them all. – we don’t want to miss a restaurant occupation
 
Once all the 35-xxxx occupations are selected, either review the table built for
you in the dashboard, or export it and inspect and make adjustments. Hover the
mouse over the upper right of the table where the red circle is below and the
“…” contains the export options
 
image020.png
 
Export into excel and you get the attached data in excel.
 
You can delete rows H and beyond, those are the PPE estimates coming from the
Utah/Wisconsin model as programed into the dashboard. We can refine these
estimates as the models improve.
 
The key think to notice is we picked up Dishwashers, Bartenders and other
occupations we might not have been aware were in the restaurant business. It is
these employee numbers that feed the model.

## Snohomish DAta and the problem with NAICS not summing (11-May-2020 Mitch)

Here is my attempt to get one small chard of the data cube nailed down for King
County.  I can scale once i have a small piece nailed down.

The attached spreadsheet came from the “County Data Tables” way down at the
bottom of this link: https://esd.wa.gov/labormarketinfo/county-profiles/king
 
I worked on the nonfarm employment tab of the spreadsheet.
 
I spent a few hours on this to get a good understanding of the hierarchy and to
make sure everything added properly.  It turns out it did not add up so well, so
I decided to investigate and force it to add up.  Now i know better what to
watch for in other data sources we might choose to use.  Also if we do get our
data from another source, I at least have one version of King County I
understand and have NAICS codes that sum properly.

There seems to be three rules needed understand and cross check the data:

1. Drill down to the most detailed level, then sum the detailed categories to
   see if they match the summary category number just above i.e., sum the
children to see if they add to the parent
2. If not, as in the spreadsheet example, I created the missing sub-category as
   “other related x” category and then it all aggregates up properly.  The
categories i created to make the sum of children equal the parent are underlined
italics in column A.
3. Once this is fixed, I only summed the totals for a particular level whether
   it is level 1, 2, 3, …6. Only sum category totals for each level.  This is a
spreadsheet example we need to use to make sure our data wranglers know how to
read the NAICS correctly. 
 
If you look at the Column AE (pink) you will see each of the most detailed
category counts.
 
For example, take cell T7 which is 1,433.9, cell v6 which is the sum of the
level 2 categories: Goods producing and Service Providing.  In level 3, I
decomposed to each of the sub-categories of these two.  You can find these in
Col x.
 
I continued through level 6, which should sum to 1,433.9 also but I must have
made slight mistake because cell AE6 is close but a little off.  I can’t spot
the error tonight, so I’ll look at it we fresh eyes tomorrow.
 
The main points are these:
- These are the rules we need to use to check the integrity of whatever data we
  download use to power the cubes.
- This will probably fix the dashboard we built to remove all the double
  counting, but fingers crossed, it might something in addition to this 
- This is a King County cross check for other data sets we may choose to use
  instead of this source.
- I now know much better exactly what to examine to decide if whatever datasets
  I am exploring are friendly to our needs.

### Not complete with astericks
Erin and i checked the data file we were using for the dashboard to figure out
how much data we have to infer. 

There are 27,020 rows with ‘**’ in the column ‘tot_emp’ of table ‘All_data’,
which means employee numbers are not available for those rows.  There are
395,647 rows in total in the dataset.

I am going to investigate those other data sources to see if i can beat this
problem another way - namely better data inputs to begin with. 


## Snohomish Anakysis (From 2020-05-19 @mitch email)
It is really difficult to get data for only Snohomish county.  In nearly all the
data sets it is part of the Seattle-Bellevue-Tacoma Metro Area.

I checked the nonmetropolitan Western Washington area that that is group of
rural counties not including Snohomish county.
 
After some digging I found the attached spreadsheet Washington State Employment
Security Department.  https://esd.wa.gov/labormarketinfo/employment-estimates
 
It has the Seattle-Bellevue-Everett MD (Metropolitan Division) and even better
breaks out a tab for Snohomish only!
 
The table is below for non-farm employment estimates in Feb 2020.  This is a key
table and we can use it as baseline or a cross-check to make sure we are about
right in labor force estimates.  (open the spreadsheet and scroll across to the
Snohomish tab)
 
One problem with these data: they are reported by NAICS. I think your model has
PPE cross-classified by OCC instead of NAICS.  Given you are pushing under a
tight deadline, I estimated the Snohomish numbers in a second way for you.  I
filtered the Erin-Mitch data cube to Seattle-Bellevue-Tacoma, which includes
Snohomish county and I multiplied by Snohomish’s proportion of the total
King-Pierce-Snohomish county populations. This produced and estimate of
approximately 400,000 people in the labor force in Snohomish county. See the
attached spreadsheet. Column I is Snohomish’s percent pro-rata based on total
county population counts.
 
So one method estimates non-farm employment in Snohomish country at
approximately 300,000 and the other estimates the total labor force of Snohomish
county at approximately 400,000.
 
Obviously, checked on the percent of the labor Force in Farming.
 
Here is the answer: Appendix II-C - Snohomish County
 
The 2000 US Census shows that out of 302,051 employed people living in Snohomish
County in 2000, 1,631 of these residents (0.5%) derived their livelihood from
farming, fishing, or forestry, making this sector the seventh largest employer
in the Snohomish County (see table below).2      Civilian labor force Employed
302,051 65.9 Management, professional, and related occupations 101,720 Sales and
office occupations 80,813 Service occupations 40,656 Production, transportation,
and material moving occupations 39,992 Construction, extraction, and maintenance
occupations 37,239 Farming, fishing, and forestry occupations 1,631
 
So the right answer is about 300,000 in the labor force.  I adjusted the
attached spreadsheet for Snohomish from the Erin-Mitch Cube to reflect this.
See column K.

![Snohomish County Analysis - image002]

## OCC Codes and Employment (@mitch 2020-05-26)
Thanks for thinking about this.
We have two items to think about –
One is the adding the sub categories and seeing if we can get everything to add up
The other is creating a view for each of 39 counties of Washington and each of the cities in Washington
 
 
The attached spreadsheet is one way to approximate a set of county data and city data.
Here is what I’ve done so far for just Washington State:
 
Assemble a list of the counties that comprise each Metropolitan Area
For example, the Seattle-Bellevue-Tacoma MSA is King, Snohomish, and Pierce Counties
Yakima MSA is just Yakima county

1. Get a total population estimate for each of the counties
2. Get a list of all the cities over 40,000, for example, and list them in the
   County where the city is located
3. Get an estimate of the Total population of the City Proper
4. Subtract all the city populations from the Counties in which they reside.
   This leaves the county population not in a city

Then we use these total population percentages to allocate the labor force data in the cube.
 
Have a look at the spreadsheet and can do a call and go over it.  The Restart
Partners group you and I are helping is going to hire an intern they ask me to
help them select the person.  I will chat with someone at 2 pm today. I would
like to hand some of stuff to their intern if they person has the data skills.
 
SO thanks for helping out with this. Have a look at the attached spreadsheet.
 
And also, I compared the Labor Force numbers coming from the BLS data cube in
the dashboard the Labor force estimate in the St. Louis Federal Research
database FRED and these comparisons are the spreadsheet too.

[Washington County data](WA Metro-Area-county cbsa-est2019-alldata.xlsx)
 

## Getting Some Data on switching to adhoc classes than NAICS or SOC (@Mitch 2020-05-15)

Thanks for fixing that summary count on dashboard. It is working well now.  The
goal is to focus on Washington State and figure out what the best data set to
use to get people cross-classified by NAICS and either SOC or OCC codes.
 
The policy experts in government don’t think in terms of “agreed to” or commonly
accepted industry or occupation codes. They think in terms of restaurants, car
washes, and landscaping, some of which might  match to a NAICS or SOC code but
often not very well.
 
Also, State-level policy makers set policies where they partially open rural
counties and delay opening metropolitan areas.  If we want to estimate PPE
needed county-by-by county, we need a county-level dataset with the labor force
classified by NAICS and SOC or OCC.
 
Washington has 39 counties and 281 incorporated cities and towns.
 
Washington has 12 metropolitan statistical areas, 9 micropolitan statistical
areas, 2 metropolitan divisions, and 1 combined statistical area.
 
If we want our dashboard to serve the needs of state, county, and city
government officials who have three needs: A need to set the restart policies
for their geographic area A need to know how many labor participants in are in
various industries and occupations in their geography A need to know how much
PPE is need daily to supply that labor force with sufficient or CDC recommended
protection
 
I think the current data and dashboard taught us a lot and it is valuable for
reporting what a particular State, consolidated metropolitan area,
non-consolidated metropolitan area, and non-Metropolitan area’s occupational
distributions are.
 
Just to make this clear: a Metro area is like Yakima, Wenatchee etc. A
Consolidated Metro Area is Seattle-Tacoma-Bellevue or Spokane-Spokane Valley
Non-metropolitan areas are collection of rural counties – see the table at the
bottom for examples for Washington State.
 
We can get occupational distributions for these geographies now from the current
dashboard and deliver to users in Excel.  I have attached three examples:
Washington State total (spreadsheet attached) 3,318,510 people in the work force
all classified by occupation.  I search for :“Police” and easily found:

i.  2,470 First-Line Supervisors of Police and Detectives
ii.      9,540 Police and Sheriff's Patrol Officers

I searched for “fire” and easily found:
i.      2,600
First-Line Supervisors of Firefighting and Prevention Workers
ii.      8,060 Firefighters
iii.      110 Fire Inspectors and Investigators
iv.      1,120 Security and Fire Alarm Systems Installers

Next I did the same thing for Yakima

(Metro Area)  – 93,570

In the labor force I searched for “construction” and

easily found these people:
i.      110 Construction Managers
ii.      3,350 Construction and Extraction Occupations
iii.      190 First-Line Supervisors of Construction Trades and Extraction Workers
iv.      560 Construction Laborers v.  100 Operating Engineers and Other Construction Equipment Operators
vi.      270 Painters, Construction and Maintenance
vii.      40 Construction and Building Inspectors

Eastern Washington non-Metro Areas – there are 96,460 in the labor
force I searched “Education”

i.      70 Education and Childcare Administrators, Preschool and Daycare
ii.      260 Education Administrators, Kindergarten through Secondary
iii.      O Education Administrators, Postsecondary
iv.  260 Educational, Guidance, and Career Counselors and Advisors
v.      10,380 Educational Instruction and Library Occupations
vi.      380 Preschool Teachers, Except Special Education
vii.      250 Kindergarten Teachers, Except Special Education
viii.      1,280 Elementary School Teachers, Except Special Education
ix.      430 Middle School Teachers, Except Special and Career/Technical Education
x.      1,000 Secondary School Teachers, Except Special and Career/Technical Education
xi.      210 Career/Technical Education Teachers, Secondary School
xii.      30 Special Education Teachers, Preschool
xiii.  140 Special Education Teachers, Kindergarten and Elementary School
xiv.      50 Special Education Teachers, Middle School
xv.      90 Special Education Teachers, Secondary School
xvi.      70 Adult Basic Education, Adult Secondary Education, and English as a Second Language Instructors
xvii.      190 Educational Instruction and Library Workers, All Other
 
This data cube delivers the labor force by occupation for State, Metro Areas,
and non-metro areas.  The good news is this data cube is up and running for the
entire county now.  Name a state, name a city, name a rural area of Wyoming and
it pumps out the labor force and occupational distribution.
 
I don’t think we need NAICS or industries by state, metro area and rural areas –
We estimate PPE by the OCC codes and we can pump out valuable reports now and
deliver them in Excel.
 
If the group agrees with this, the next steps is to assign PPE usage per person
per day and we can do the multiplication and it comes with the download into
Excel.
 
We can abbreviate the task if we think everyone in the “education” “police” or
“construction” categories will get the same approximate of PPE usage per day per
person. We can discuss how much time we want to do detailed or refined estimates
in the first pass.
 
Here are the Washington State Non-Metropolitan Areas:
 

## Marketing and the NOCOVID (National Organizing Coalition on Virus Information Distribution nocovid.us, @mitch, 2020-05-12

I was working to setup some tests for COVID messaging to various demographic
groups and mindsets. I sent a note to my research buddy, Jon Puleston, in the UK
with whom I have completes some personality testing and messaging work on other
topics. I suggested we start doing some preliminary data collection. He was
digging around and wrote a note to Christopher Graves at Ogilvy, a person we
have both worked with in the past, and Christopher came to us with an super
useful and insightful document (attached). Chris is working with the NOCOVID
organization.

The document comes from this group:

NOVOVID 
National Organizing Coalition On Virus Information Distribution  
https://nocovid.us

It seems like an organization, marketing, and messaging approach we need to
consider. We may want to partner with this group and use to them as a channel to
inform our own approach. 

Here is Christopher's note back to Jon and me - (Note: Ogilvy is a WPP owned company)

Jon,
Thanks for sharing and Mitch, great to reconnect.I'd love to keep collaborating
on COVID. I am supporting Gates Foundation, UNICEF, WHO and NOCOVID (elite power
bunch in the US of mayors, governors, scientists, doctors, Hollywood). 
 
I was just asked about the UK new messaging. Here were my quick thoughts:
 
On the UK messaging, here's a good PR roundup. 
 
From my POV and BeSci, some thoughts:
 
1. Concreteness is needed not abstraction. People must be able to picture your
   demand/request/recommendation. "Stay at home" and "keep 1 meter apart" can be
easily pictured. "Stay alert" is a state of vigilance and very abstract. It is
intransitive. It is being not doing.
2. Humans value avoiding a loss at 2x to 3x the power of a gain (Prospect
Theory"). So frame the work already done by the NHS and the public as ground
that has been taken from the enemy and ground you will not give up now.
3. "Goal gradient" is a BeSci effect that visually shows people the progress
   they are making. The closer to the goal, the more engagement takes place.
Show how far we have come with our actions so far. 
4. My Messaging: "Stand your ground. Don't give up now. Keep apart no matter
   what. We have saved thousands of lives, don't abandon them now " 

End of Chris's Message. 

The RestartSafe group needs to evaluate cooperating with this group and how it
fits with our agenda.  I can reach out to Christopher and that group if
appropriate.  Have a look at the attachment; it is and excellent part of the
tool kit. 


(NOCOVID Toolkit)[NOCOVID toolkit for Local Leaders (Newport News-Hampton VA).pdf]


