#!/usr/bin/env python
# coding: utf-8

# # Cleaning the Data
# 

# Since the original csv file is too large to store in git hub, we split it into 4 parts and concatenated it using pandas to reconstruct it as needed.

# ## Dependencies 

# In[3]:


# Import dependencies
import pandas as pd
import numpy as np
import os 


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


# In[6]:


# homicide_df2 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 200001) & (MasterHomicide_df['index']<= 400000),:]
# homicide_df2.to_csv("ProjectData/MurderData2.csv", index=False)


# In[7]:


# homicide_df3 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 400001) & (MasterHomicide_df['index']<= 600000),:]
# homicide_df3.to_csv("ProjectData/MurderData3.csv", index=False)


# In[8]:


# homicide_df4 = MasterHomicide_df.loc[(MasterHomicide_df['index']>= 600001) & (MasterHomicide_df['index']<= 800000),:]
# homicide_df4.to_csv("ProjectData/MurderData4.csv", index=False)


# ## Rebuilding the Dataset

# * The following code is used to reconstruct the original data file using Pandas' concatenate

# In[4]:


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


# ## Createing the Midwest Murder Dataset

# * The following code is used to create the midwest murder dataset

# In[5]:


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


# In[6]:


#create midwest murder data csv
midwest_homicide_df.to_csv("MidwestMurderData.csv", index=False)


# ## Creating a Technology Timeline

# The events in the technology timeline events were sourced from three websites:
# 
# • https://www.explainthatstuff.com/timeline.html
# 
# • https://policetechnology.wordpress.com/timeline-of-technology/
# 
# • http://www.softschools.com/timelines/forensic_science_timeline/99/
# 

# In[7]:


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


# ## Creating a President dataset 
# Sourced data from wikipedia. Handmade in Microsoft Excel

# In[10]:


#create President Dataframe
pfile = os.path.join('ProjectData','Presidents.csv')
pcsv = pd.read_csv(pfile, encoding = 'unicode_escape')
pres_df = pd.DataFrame(pcsv)
pres_df.head()


# ## Eric's Dataframes

# In[8]:


#create dataframes by year, solved, unsolved, and total from the midwest_homocide dataset
mwYearSolved_df = midwest_homicide_df[['Year','Solved']]
mSolved_df = mwYearSolved_df.loc[mwYearSolved_df['Solved']=='Yes',:].groupby(['Year']).count()
mUnsolved_df = mwYearSolved_df.loc[mwYearSolved_df['Solved']=='No',:].groupby(['Year']).count()
mUnsolved_df.columns = (['Unsolved'])

#merge solved and unsolved dataframes
murders_by_year_df = mSolved_df.merge(mUnsolved_df, on = 'Year', how = 'inner')
murders_by_year_df['Total'] = murders_by_year_df['Solved'] + murders_by_year_df['Unsolved']
murders_by_year_df.head()


# In[11]:


#merge president Dataframe with murders dataframe
pres_mby_df = murders_by_year_df.merge(pres_df, on = 'Year', how = 'inner')
pres_mby_df.head()


# In[13]:


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


# In[15]:


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


# In[17]:


#remove 1 year presidents
r_pres_mby_df = pres_mby_df.loc[(pres_mby_df['Year']>1976) & (pres_mby_df['Year']<= 2016),:]
r_pres_mby_df.tail()


# In[18]:


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


# In[ ]:




