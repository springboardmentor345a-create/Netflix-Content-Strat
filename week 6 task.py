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


# In[12]:


from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

le = LabelEncoder()

df['rating_encoded'] = le.fit_transform(df['rating'])
df['type_encoded'] = le.fit_transform(df['type'])

features = df[['rating_encoded','type_encoded']]

kmeans = KMeans(n_clusters=3)

df['cluster'] = kmeans.fit_predict(features)

print(df[['title','cluster']].head())


# In[13]:


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X = df[['rating_encoded']]
y = df['type_encoded']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = DecisionTreeClassifier()

model.fit(X_train,y_train)

print("Accuracy:",model.score(X_test,y_test))

