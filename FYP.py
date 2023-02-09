#!/usr/bin/env python
# coding: utf-8

# In[1]:


# convert to CSV
import mplsoccer
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# load in dataset and split to one player
dataset = pd.read_csv('data/987601.csv')
attributes = ['FrameID', 'ID', '7X', '7Y']

xy_values = dataset.loc[:, attributes]

# select every 750th row between two values ie. every 30 seconds
first_half = xy_values.iloc[5913:78676]
player7_first_half = first_half.iloc[::750, :]

# scale up the data
player7_first_half['7X'] = player7_first_half['7X'] + 5550
player7_first_half['7Y'] = player7_first_half['7Y'] + 4400


# In[3]:


import seaborn as sns
from mplsoccer.pitch import Pitch

pitch = mplsoccer.Pitch(pitch_type='custom', pitch_length=11100, pitch_width=8800, pitch_color='green', line_color='white', axis =True, label=True)
fig,ax = pitch.draw(figsize=(111,88))

#player 7 heatmap of the first half
pitch.kdeplot(player7_first_half['7X'], player7_first_half['7Y'], ax=ax, cmap='Reds', fill=True)


# In[4]:


# Player 7 heatmap of the second half
second_half = xy_values.iloc[101875:175613]
player7_second_half = second_half.iloc[::750, :]

# scale up the data
player7_second_half['7X'] = player7_second_half['7X'] + 5550
player7_second_half['7Y'] = player7_second_half['7Y'] + 4400

fig,ax = pitch.draw(figsize=(111,88))
pitch.kdeplot(player7_second_half['7X'], player7_second_half['7Y'], ax=ax, cmap='Reds', fill=True)


# In[ ]:





# In[ ]:




