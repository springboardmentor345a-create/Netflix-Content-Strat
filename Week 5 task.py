#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

df = pd.read_csv("netflix_titles.csv")
df.head()


# In[5]:


from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans

le = LabelEncoder()

df['rating_encoded'] = le.fit_transform(df['rating'])
df['type_encoded'] = le.fit_transform(df['type'])

features = df[['rating_encoded','type_encoded']]

kmeans = KMeans(n_clusters=3)

df['cluster'] = kmeans.fit_predict(features)

print(df[['title','cluster']].head())


# In[6]:


from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier

X = df[['rating_encoded']]
y = df['type_encoded']

X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.2)

model = DecisionTreeClassifier()

model.fit(X_train,y_train)

print("Accuracy:",model.score(X_test,y_test))


# In[7]:


df[['title','cluster']].head()


# In[ ]:





# In[ ]:




