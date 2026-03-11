#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd

df = pd.read_csv("netflix_titles.csv")
df.head()


# In[3]:


country_count = df['country'].value_counts()
print(country_count)


# In[4]:


import matplotlib.pyplot as plt

country_count.head(10).plot(kind='bar')
plt.title("Top 10 Countries Producing Netflix Content")
plt.show()


# In[8]:


df['duration'] = df['duration'].astype(str)

df['duration_num'] = df['duration'].str.extract('(\d+)').astype(float)


# In[9]:


df['content_origin'] = df['director'].apply(
    lambda x: 'Original' if x != 'unknown' else 'Licensed'
)


# In[10]:


df['length_category'] = df['duration_num'].apply(
    lambda x: 'Short' if x < 60 else
              'Medium' if x < 120 else
              'Long'
)


# In[11]:


df[['duration','duration_num','length_category']].head()


# In[14]:


df['content_origin'].value_counts()


# In[15]:




