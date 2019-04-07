#!/usr/bin/env python
# coding: utf-8

# # Cleaning the Data
# 

# Since the original csv file is too large to store in git hub, we split it into 4 parts and concatenated it using pandas to reconstruct it as needed.

# ## Dependencies 

# In[1]:


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

# In[10]:


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


# ## Createing t

# * The following code is used to create the midwest murder dataset

# In[11]:


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


# In[12]:


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

# In[13]:


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
slvd_impact


# ## Creating a President dataset 

# In[14]:


#create President Dataframe
pfile = os.path.join('ProjectData','Presidents.csv')
pcsv = pd.read_csv(pfile, encoding = 'unicode_escape')
pres_df = pd.DataFrame(pcsv)
pres_df.head()


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




