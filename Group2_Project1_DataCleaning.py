#!/usr/bin/env python
# coding: utf-8

# In[2]:


# Import dependencies
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import scipy.stats as stats
import os 

# Import cleaned midwest data
file = os.path.join('MidwestMurderData.csv')

# Read into DataFrame
midwest_homicide_df = pd.read_csv(file)
midwest_homicide_df.head()


# In[3]:


midwest_homicide_df.columns


# ### Create data frame of total homicides per year.

# In[7]:


midwest_total = midwest_homicide_df[['Year', 'ID']]
midwest_total_group = midwest_total.groupby(['Year']).count().reset_index()
midwest_total_group.head()


# ### Preparing data for visualizations about homicide solve rates.

# In[4]:


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


# In[5]:


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


# In[6]:


# Create a DataFrame for each city
chicago = new_df[new_df["City"] == 'Chicago-Naperville-Joliet, IL-IN-WI']
indy = new_df[new_df["City"] == 'Indianapolis, IN']
mpls = new_df[new_df["City"] == 'Minneapolis-St. Paul-Bloomington, MN-WI']


# In[ ]:




