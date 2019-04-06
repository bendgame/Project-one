
import pandas as pd
import numpy as np
import os 

file = os.path.join('SHR76_17.csv')
homicide_df = pd.read_csv(file)
homicide_df.head()

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

midwest_homicide_df = homicide_df[homicide_df['State'].isin(midwest_states)]