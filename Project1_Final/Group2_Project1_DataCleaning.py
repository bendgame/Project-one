#!/usr/bin/env python
# coding: utf-8

# # Cleaning the Data
# 

# Since the original csv file is too large to store in git hub, we split it into 4 parts and concatenated it using pandas to reconstruct it as needed.

# In[1]:


# Import dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import os 
import requests

from census import Census

# Census API Key
from config import api_key
c = Census(api_key, year=2009)


# ## Splitting the Dataset to store it on GitHub

# * Uncomment if loading the original file from the zip. The path assumes both the unzipped file and the repo exist on the desktop.

# In[2]:


#Load the original data file. The datafile is zipped in the repo since it is too large to store. 

# file = os.path.join('..','SHR76_17.csv')
# MasterHomicide_df = pd.read_csv(file)
# MasterHomicide_df.head()


# In[3]:


#MasterHomicide_df = MasterHomicide_df.reset_index()


# * The following code was used to split the master file into 4 parts so it could be loaded onto the remote github repo

# In[4]:


# homicide_df1 = MasterHomicide_df.loc[MasterHomicide_df['index']<=200000,:]
# homicide_df1.to_csv("ProjectData/MurderData1.csv", index=False)


# In[5]:


# homicide_df2 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 200001) & (MasterHomicide_df['index']<= 400000),:]
# homicide_df2.to_csv("ProjectData/MurderData2.csv", index=False)


# In[6]:


# homicide_df3 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 400001) & (MasterHomicide_df['index']<= 600000),:]
# homicide_df3.to_csv("ProjectData/MurderData3.csv", index=False)


# In[7]:


# homicide_df4 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 600001) & (MasterHomicide_df['index']<= 800000),:]
# homicide_df4.to_csv("ProjectData/MurderData4.csv", index=False)


# ## Rebuilding the Dataset

# * The following code is used to reconstruct the original data file using Pandas' concatenate

# In[8]:


m1 = pd.read_csv("ProjectData/MurderData1.csv")
m1_df = pd.DataFrame(m1)

m2 = pd.read_csv("ProjectData/MurderData2.csv")
m2_df = pd.DataFrame(m2)

m3 = pd.read_csv("ProjectData/MurderData3.csv")
m3_df = pd.DataFrame(m3)

m4 = pd.read_csv("ProjectData/MurderData4.csv")
m4_df = pd.DataFrame(m4)

a = m1_df
b = m2_df
c = m3_df
d = m4_df
#a.index = x.index  # make duplicate indices!
murderData1_df = pd.concat([a, b])
murderData2_df = pd.concat([murderData1_df, c])
homicide_df = pd.concat([murderData2_df, d])

homicide_df.head()
len(homicide_df)


# ## Creating the Midwest Murder Dataset

# * The following code is used to create the midwest murder dataset

# In[9]:


#create a list of midwest states
midwest_states = ['Minnesota',
                  'Kansas',
                  'Nebraska',
                  'Iowa',
                  'South Dakota',
                  'North Dakota',
                  'Wisconsin',
                  'Michigan',
                  'Indiana',
                  'Ohio',
                  'Missouri',
                  'Illinois']

#create the dataframe for the midwest states from the original data
midwest_homicide_df = homicide_df[homicide_df['State'].isin(midwest_states)]
midwest_homicide_df = midwest_homicide_df.drop(columns = 'index', axis = 1)
midwest_homicide_df = midwest_homicide_df.reset_index(drop = True)
midwest_homicide_df.head()


# In[10]:


#create midwest murder data csv
midwest_homicide_df.to_csv("MidwestMurderData.csv", index=False)


# In[11]:


# Import cleaned midwest data
file = os.path.join('MidwestMurderData.csv')

# Read into DataFrame
midwest_homicide_df = pd.read_csv(file)
midwest_homicide_df.head()


# In[12]:


midwest_homicide_df.columns


# ### Create data frame of total homicides per year.

# In[13]:


midwest_total = midwest_homicide_df[['Year', 'ID']]
midwest_total_group = midwest_total.groupby(['Year']).count().reset_index()
midwest_total_group.head()


# ### Set up data frames for victim and offender demographics.

# In[14]:


# Get count of sex of offenders for all cases
offender_gender = pd.DataFrame(midwest_homicide_df, columns = ['OffSex'])
count_offender_gender = offender_gender.stack().value_counts()


# In[15]:


# Get count of sex of victims for all cases
gender = pd.DataFrame(midwest_homicide_df, columns = ['VicSex']) 
count_gender = gender.stack().value_counts()


# In[16]:


# Get count of race of victims for all cases
race = pd.DataFrame(midwest_homicide_df, columns = ['VicRace']) 
victim_race = race.stack().value_counts()


# In[17]:


# Get count of race of offenders for all cases
off_race = pd.DataFrame(midwest_homicide_df, columns = ['OffRace']) 
offender_race = off_race.stack().value_counts()


# ### Preparing DataFrames of victim/offender relationships.

# In[18]:


#Create a dataframe with only the columns I'm interested in
relationship_df = midwest_homicide_df[['Relationship', 'VicSex','Weapon', 'OffSex']]


#Split the weapons into "close contact" and "minimal contact" categories
relationship_df['Weapon'] = relationship_df['Weapon'].replace(
                                                {"Knife or cutting instrument": "Close Contact",
                                                "Handgun - pistol, revolver, etc": "No/Little Contact",
                                                "Shotgun": "No/Little Contact",
                                                "Strangulation - hanging": "No/Little Contact",
                                                "Personal weapons, includes beating": "Close Contact",
                                                "Blunt object - hammer, club, etc" : "Close Contact",
                                                "Rifle": "No/Little Contact",
                                                "Firearm, type not stated": "No/Little Contact",
                                                "Asphyxiation - includes death by gas": "Close Contact",
                                                "Other gun": "No/Little Contact",
                                                "Fire": "No/Little Contact",
                                                "Drowning": "Close Contact",
                                                "Pushed or thrown out window": "No/Little Contact",
                                                "Narcotics or drugs, sleeping pills": "No/Little Contact",
                                                "Explosives": "No/Little Contact",
                                                "Poison - does not include gas": "No/Little Contact"})

#Combine similar relationships together for the male and female victim charts
relationship_df['Relationship'] = relationship_df["Relationship"].replace(
                                                  {'Brother': 'Sibling',
                                                   'Sister': 'Sibling',
                                                   'Father': 'Parent',
                                                   'Mother': 'Parent',
                                                   'Daughter': 'Child',
                                                   'Son': 'Child',
                                                   'Stepson': 'Child',
                                                   "Stepdaughter": "Child",
                                                   "Homosexual relationship": 'Partner',
                                                   "Boyfriend" : "Partner",
                                                   "Girlfriend" : "Partner",
                                                   "Common-law husband" : "Partner",
                                                   "Common-law wife" : "Partner",
                                                   "Ex-husband" : "Spouse",
                                                   "Ex-wife" : "Spouse",
                                                   "Stepmother" : "Parent",
                                                   "Stepfather" : "Parent",
                                                   "Husband" : "Spouse",
                                                   "Wife" : "Spouse",
                                                  "Friend": 'Other - known to victim',
                                                  "Neighbor": 'Other - known to victim',
                                                  "Employee": 'Other - known to victim',
                                                  "Employer": 'Other - known to victim',
                                                  "In-law" : 'Other - known to victim'})


# In[19]:


#Female Datafarme - pull out only female victims
victims_df = relationship_df[['Relationship', 'VicSex']]
female_victims = victims_df.loc[victims_df["VicSex"]=='Female', :]

#Group Female Victims by Relationships
female_victims = female_victims.groupby('Relationship').count()

#Rename columns
female_victims_df = female_victims.rename(columns={"VicSex": "Female Victim"})

#Sort values so graphs are in ascending order
female_df = female_victims_df.reset_index().sort_values("Female Victim")

#Drop the highest outlier value: Relationship Undefined
female_df = female_df.drop(6)

#Find the sum of all Female Victims
female_df.sum()

#Calculate the percentage of female victims by relationship (23810 is the sum of all female victims)
female_percent = female_df['Female Victim']/23810*100
female_percent = female_percent.round()


# In[20]:


#Male Dataframe - Pull out only Male Victims
male = victims_df.loc[victims_df["VicSex"] == "Male", :]

#Group Male Victims by Relationships
male_victims = male.groupby('Relationship').count()

#Rename Columns
male_victims_df = male_victims.rename(columns={"VicSex": "Male Victim"})


#Sort values so graphs are in ascending order
male_df = male_victims_df.reset_index().sort_values("Male Victim")

#Drop the highest outlier value: Relationship Undefined
male_df = male_df.drop(6)

#Find the sum of all Male Victims
male_df.sum()

#Calculate the percentage of male victims by relationship (23810 is the sum of all female victims)
male_percent = male_df['Male Victim']/63925*100
male_percent = male_percent.round()


# ### Victim relationships and murder weapons.

# In[21]:


##GROUP WEAPON TYPE AND VICTIM RELATIONSHIP##
#--------
#Adjust relationship groups to reflect aquaintance, stranger, family, and romantic partner
close_contact = relationship_df[['Relationship', 'Weapon']]
close_contact['Relationship'] = close_contact['Relationship'].replace(
                                            {'Spouse': 'Romantic Partner',
                                            'Sibling': 'Family Member',
                                            'Parent': 'Family Member',
                                            'Child': 'Family Member',
                                            'Partner': 'Romantic Partner',
                                            'Other family': 'Family Member'})

#Find only the close contact weapon types grouped by relationship
close_contact = close_contact[close_contact.Weapon == 'Close Contact'].groupby('Relationship').count()
close_contact = close_contact.rename(columns={'Weapon': 'Close Contact'})

#--------
#Group together the minimal contact weapon types by relationship
minimal_contact= relationship_df[['Relationship', 'Weapon']]

#Adjust relationship groups to reflect aquaintance, stranger, family, and romantic partner
minimal_contact['Relationship'] = minimal_contact['Relationship'].replace(
                                            {'Spouse': 'Romantic Partner',
                                            'Sibling': 'Family Member',
                                            'Parent': 'Family Member',
                                            'Child': 'Family Member',
                                            'Partner': 'Romantic Partner',
                                            'Other family': 'Family Member'})

#Group minimal_contact weapons by relationshps
minimal_contact = minimal_contact[minimal_contact.Weapon == 'No/Little Contact'].groupby('Relationship').count()
minimal_contact = minimal_contact.rename(columns={'Weapon': 'No/Little Contact'})


#Merge the two types of weapons together based on relationship, reset index, drop "relatioship not determined"
weapon_type = pd.merge(close_contact, minimal_contact, how='outer', on=['Relationship']).reset_index()
weapon_type = weapon_type.drop(2)
weapon_type = weapon_type.drop(3)


# In[22]:


#Show dataframe for pie chart 
weapon_type


# ### Preparing data for visualizations about homicide solve rates.

# In[23]:


# Remove unneccessary columns
midwest_solved = midwest_homicide_df[['Year', 'Solved']]

# Group by year to get count of total homicides per year
midwest_year_group = midwest_solved.groupby(['Year']).count()

# Remove unsolved cases to get count of solved cases per year
solved = midwest_solved.loc[midwest_solved["Solved"] == "Yes"]
midwest_solved_group = solved.groupby(['Year']).count()

# Calculate solve rate
midwest_solved_group["% Solved"] = midwest_solved_group["Solved"] / midwest_year_group["Solved"] * 100
midwest_solved_group = midwest_solved_group.reset_index(drop=False)

midwest_solved_group.head()


# In[24]:


# Choose three cities to look at 
midwest_cities = ['Chicago-Naperville-Joliet, IL-IN-WI',
                  'Indianapolis, IN',
                  'Minneapolis-St. Paul-Bloomington, MN-WI',]

# Remove unneccessary columns from original DataFrame
cities_df = midwest_homicide_df[['MSA', 'Year', 'Solved']]

# Pull out three specified cities
cities_df = cities_df[cities_df['MSA'].isin(midwest_cities)]
cities_df = cities_df.reset_index(drop=True)

# Group by city and year to get total count of homicide cases
cities_year_group = cities_df.groupby(['MSA', 'Year']).count().reset_index()

# Remove unsolved cases to get count of solved cases
cities_solved = cities_df.loc[cities_df["Solved"] == "Yes"]
cities_solved = cities_solved.groupby(['MSA', 'Year']).count().reset_index()

# Merge DataFrames
new_df = pd.merge(cities_solved, cities_year_group,  how='outer', left_on=['MSA','Year'], right_on = ['MSA','Year'])

# Rename columns
new_df = new_df.rename(columns={'MSA': 'City', 
                                'Solved_x': 'Homicides Solved',
                                'Solved_y': 'Total Homicides'})

# Calculate solve rates
new_df["% Solved"] = new_df["Homicides Solved"] / new_df["Total Homicides"] * 100
new_df.head()


# In[25]:


# Create a DataFrame for each city
chicago = new_df[new_df["City"] == 'Chicago-Naperville-Joliet, IL-IN-WI']
indy = new_df[new_df["City"] == 'Indianapolis, IN']
mpls = new_df[new_df["City"] == 'Minneapolis-St. Paul-Bloomington, MN-WI']


# ### Creating a Technology Timeline
# The events in the technology timeline events were sourced from three websites:
# 
# • https://www.explainthatstuff.com/timeline.html
# 
# • https://policetechnology.wordpress.com/timeline-of-technology/
# 
# • http://www.softschools.com/timelines/forensic_science_timeline/99/

# In[26]:


#load the technology timeline
tfile = os.path.join('ProjectData','TechnologyTimeline.csv')
tcsv = pd.read_csv(tfile, encoding = 'unicode_escape')

#create technology dataframe
tech_df = pd.DataFrame(tcsv)

#sort data by year
tech_df = tech_df.sort_values(['Year'])

#match the start year to the murder dataset
tech_df = tech_df.loc[tech_df['Year'] >= 1976,:]

#select events in which we predict an impact on solved murder
slvd_impact = tech_df.loc[tech_df['Predicted Impact'] == 'yes',:]
slvd_impact.head()


# In[ ]:





# ### Creating a President dataset 
# Sourced data from wikipedia. Handmade in Microsoft Excel

# In[27]:


#create President Dataframe
pfile = os.path.join('ProjectData','Presidents.csv')
pcsv = pd.read_csv(pfile, encoding = 'unicode_escape')
pres_df = pd.DataFrame(pcsv)
pres_df.head()


# In[28]:


#create dataframes by year, solved, unsolved, and total from the midwest_homocide dataset
mwYearSolved_df = midwest_homicide_df[['Year','Solved']]
mSolved_df = mwYearSolved_df.loc[mwYearSolved_df['Solved']=='Yes',:].groupby(['Year']).count()
mUnsolved_df = mwYearSolved_df.loc[mwYearSolved_df['Solved']=='No',:].groupby(['Year']).count()
mUnsolved_df.columns = (['Unsolved'])

#merge solved and unsolved dataframes
murders_by_year_df = mSolved_df.merge(mUnsolved_df, on = 'Year', how = 'inner')
murders_by_year_df['Total'] = murders_by_year_df['Solved'] + murders_by_year_df['Unsolved']
murders_by_year_df.head()


# In[29]:


#merge president Dataframe with murders dataframe
pres_mby_df = murders_by_year_df.merge(pres_df, on = 'Year', how = 'inner')
pres_mby_df.head()


# In[30]:


#create dataframe for calculating the average murder per year by presidency
presMurders_df = pres_mby_df.groupby(['President', 'Party']).sum().reset_index()
presTerms_df = pres_mby_df.groupby(['President']).count().reset_index()
presTerms_df = presTerms_df[['President', 'Year']]
presTerms_df.columns = ('President','Years')
presTerms_murder_df = presTerms_df.merge(presMurders_df, on = 'President', how = 'inner')
presTerms_murder_df['Avg Murder per Year'] = presTerms_murder_df['Total'] / presTerms_murder_df['Years']
presTerms_murder_df[['President', 'Years', 'Solved', 'Unsolved', 'Total', 'Avg Murder per Year']]


#sort the data in order of presidency
presidents = ['Gerald R. Ford', 'Jimmy Carter', 'Ronald Reagan', 'George Bush', 'Bill Clinton', 'George W Bush', 'Barack Obama', 'Donald Trump']
mapping = {president: i for i, president in enumerate(presidents)}
key = presTerms_murder_df['President'].map(mapping)    
order_presTerms_murder_df = presTerms_murder_df.iloc[key.argsort()]

order_presTerms_murder_df.head()


# In[31]:


#group data by party counts
party_counts_df = pres_mby_df[['Party', 'Year']]
party_counts_df = party_counts_df.groupby(['Party']).count()
party_counts_df.columns = ['Total Years']
party_counts_df.head()

#group data by summed values
mrdr_party_df = pres_mby_df[['Solved', 'Unsolved', 'Total', 'Party']]
mrdr_party_df = mrdr_party_df.groupby(['Party']).sum()
mrdr_party_df.head()

#merge dataframes
mrdr_party_t_df = mrdr_party_df.merge(party_counts_df, on ='Party', how = 'inner')

#calculate average
mrdr_party_t_df['Avg Murders by Party'] = round(mrdr_party_t_df['Total'] / mrdr_party_t_df['Total Years'])
mrdr_party_t_df = mrdr_party_t_df.reset_index()
mrdr_party_t_df


# In[32]:


#remove 1 year presidents
r_pres_mby_df = pres_mby_df.loc[(pres_mby_df['Year']>1976) & (pres_mby_df['Year']<= 2016),:]
r_pres_mby_df.tail()


# In[33]:


#create the revised dataset
r_party_counts_df = r_pres_mby_df[['Party', 'Year']]
r_party_counts_df = r_party_counts_df.groupby(['Party']).count()
r_party_counts_df.columns = ['Total Years']
r_party_counts_df.head()

#group data by summed values
r_mrdr_party_df = r_pres_mby_df[['Solved', 'Unsolved', 'Total', 'Party']]
r_mrdr_party_df = r_mrdr_party_df.groupby(['Party']).sum()
r_mrdr_party_df.head()

#merge 
r_mrdr_party_t_df = r_mrdr_party_df.merge(r_party_counts_df, on ='Party', how = 'inner')
#r_mrdr_party_t_df['Expected Murders'] = r_mrdr_party_t_df['Total'].mean()
r_mrdr_party_t_df['Avg Murders per Year'] = r_mrdr_party_t_df['Total'] / r_mrdr_party_t_df['Total Years']
r_mrdr_party_t_df = r_mrdr_party_t_df.reset_index()
r_mrdr_party_t_df


# ### Adding census data to calculate murder rate per capita.

# In[34]:


import requests

from census import Census

# Census API Key
from config import api_key
c = Census(api_key, year=2009)


# In[35]:


# From 2009 census, the same year from which MSA codes/labels in midwest_homicide_df were taken, grab metro populations
# Filter and clean census metro data to get just the metro areas that match those in midwest_homicide_df above

acs_msa = c.acs5.get(('NAME', 'B01003_001E'),                     {'for': 'metropolitan statistical area/micropolitan statistical area:*'})
acs_msa_df = pd.DataFrame(acs_msa)
acs_msa_df = acs_msa_df.rename(columns={"B01003_001E": "Population", "NAME": "MSA1",
                                  "metropolitan statistical area/micropolitan statistical area": "MSA Code"})

# Limit results to metro areas, excluding census 'micropolitan areas'
# The Murder Accountability Project processed census data through SPSS, changing MSA codes to labels
# All micropolitan MSA codes became "Rural {Statename}", with no way for users to match them back to orig codes
acs_metroonly = acs_msa_df[acs_msa_df['MSA1'].str.contains('Metro Area')]
acs_metroonly = acs_metroonly.reset_index(drop=True)

# New df with split value columns to isolate 'Metro Area'
new_metro = acs_metroonly["MSA1"].str.split(" Metro Area", n = 1, expand = True)  
# Making separate MSA column from new df 
acs_metroonly["MSA"]= new_metro[0] 
# Dropping old MSA columns 
acs_metroonly.drop(columns =["MSA1"], inplace = True) 

# New df with split columns to isolate state abbreviations
metrostates = acs_metroonly["MSA"].str.split(", ", n = 1, expand = True) 
# Add separate state column from new df
acs_metroonly['State'] = metrostates[1]

# Create list of unique values in state column to identify all possible midwest state labels in MidwestMurderData.csv
stateslist = acs_metroonly['State'].unique().tolist() 
midweststates = ['OH-PA', 'KS', 'WV-OH', 'WI', 'IA', 'OH', 'IN', 'MO', 'IL', 'IN-MI', 'SD', 'IA-NE-SD',                   'MO-IL', 'MO-KS', 'MN', 'MI', 'NE-IA', 'MN-WI', 'KY-IN', 'NE', 'WI-MN', 'WV-KY-OH',                   'ND-MN', 'AR-MO', 'IN-KY', 'IA-IL', 'OH-KY-IN', 'IL-IN-WI', 'ND']
# New df with just state values in the midweststates list, reset index 
midwest_metros = acs_metroonly[acs_metroonly['State'].isin(midweststates)]
midwest_metros = midwest_metros.reset_index(drop=True)

# Print census summary table
with pd.option_context('display.max_rows', None, 'display.max_columns', None):
    print(midwest_metros)


# In[36]:


# Back in the midwest murder dataframe, get murder counts for each MSA
# Do this just murders in 2005-2009 (same year as our 5-year census estimates)

# Create df for 2005 through 2009 only
acs_years = [2005, 2006, 2007, 2008, 2009]
midwest_homicide_df_0509 = midwest_homicide_df[midwest_homicide_df['Year'].isin(acs_years)]

# Count murders for each metro area
msa_0509_murdercounts = midwest_homicide_df_0509.groupby(['MSA']).count().reset_index()

# Trim to necessary fields
msa_0509_murdercounts = msa_0509_murdercounts[['MSA', 'ID']]

# Remove areas derived from aggregations of all micropolitan areas in each state
msa_0509_murdercounts = msa_0509_murdercounts.rename(columns={'ID': 'Homicides', 'MSA': 'MSA'})
msa_0509_murders_urban = msa_0509_murdercounts[~msa_0509_murdercounts['MSA'].str.contains('Rural ')]
msa_0509_murders_urban = msa_0509_murders_urban.reset_index(drop=True)


# In[37]:


# Add murder counts, for all years and for 2009 only, to census df with 2009 population estimates
# Sort Census summary table alphabetically to match the murder data
midwest_metros = midwest_metros.sort_values('MSA').reset_index(drop=True)

# Merge the two dfs
midwest_metromurders = pd.merge(midwest_metros, msa_0509_murders_urban, on='MSA', how='outer')
midwest_metromurders = midwest_metromurders.rename(columns={
    'MSA': 'Metro area', 'Homicides': 'Murders 2005-2009', 'Population': 'Population 2009', \
    'MSA Code': 'MSA Code', 'State': 'State',
})
midwest_metromurders = midwest_metromurders.dropna()

midwest_metromurders_0509 = midwest_metromurders[['Metro area', 'Population 2009', 'Murders 2005-2009']]


# In[ ]:




