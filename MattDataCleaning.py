#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
from census import Census
# Census API Key
from config import api_key
c = Census(api_key, year=2009)


# In[2]:


midwest_murders = pd.read_csv('MidwestMurderData.csv')


# In[3]:


# From 2009 census, the same year from which MSA codes/labels in midwest_murders were taken, grab metro populations
# Filter and clean census metro data to get just the metro areas that match those in midwest_murders above

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


# In[4]:


# Back in the midwest murder dataframe, get murder counts for each MSA
# Do this just murders in 2005-2009 (same year as our 5-year census estimates)

# Create df for 2005 through 2009 only
acs_years = [2005, 2006, 2007, 2008, 2009]
midwest_murders_0509 = midwest_murders[midwest_murders['Year'].isin(acs_years)]

# Count murders for each metro area
msa_0509_murdercounts = midwest_murders_0509.groupby(['MSA']).count().reset_index()

# Trim to necessary fields
msa_0509_murdercounts = msa_0509_murdercounts[['MSA', 'ID']]

# Remove areas derived from aggregations of all micropolitan areas in each state
msa_0509_murdercounts = msa_0509_murdercounts.rename(columns={'ID': 'Homicides', 'MSA': 'MSA'})
msa_0509_murders_urban = msa_0509_murdercounts[~msa_0509_murdercounts['MSA'].str.contains('Rural ')]
msa_0509_murders_urban = msa_0509_murders_urban.reset_index(drop=True)


# In[5]:


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




