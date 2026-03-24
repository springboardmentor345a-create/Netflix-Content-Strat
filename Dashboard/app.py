import streamlit as st
import pandas as pd
import plotly.express as px

# Load dataset
df = pd.read_csv("netflix_cleaned_final.csv")

st.title("🎬 Netflix Content Dashboard")

# ---------------- FILTERS ----------------
year = st.sidebar.multiselect("Select Year", df['release_year'].unique())
genre = st.sidebar.multiselect("Select Genre", df['genre'].unique())
country = st.sidebar.multiselect("Select Country", df['country'].unique())
ctype = st.sidebar.multiselect("Content Type", df['type'].unique())

# Apply filters
filtered_df = df.copy()

if year:
    filtered_df = filtered_df[filtered_df['release_year'].isin(year)]
if genre:
    filtered_df = filtered_df[filtered_df['genre'].isin(genre)]
if country:
    filtered_df = filtered_df[filtered_df['country'].isin(country)]
if ctype:
    filtered_df = filtered_df[filtered_df['type'].isin(ctype)]

# ---------------- VISUALS ----------------

# 1. Content Type Distribution
fig1 = px.pie(filtered_df, names='type', title="Content Type Distribution")
st.plotly_chart(fig1)

# 2. Top Genres per Year
genre_year = filtered_df.groupby(['release_year', 'genre']).size().reset_index(name='count')
fig2 = px.bar(genre_year, x='release_year', y='count', color='genre',
              title="Top Genres per Year")
st.plotly_chart(fig2)

# 3. Content by Country
country_count = filtered_df['country'].value_counts().reset_index()
country_count.columns = ['country', 'count']
fig3 = px.bar(country_count.head(10), x='country', y='count',
              title="Top Countries")
st.plotly_chart(fig3)

# 4. Rating Analysis
fig4 = px.histogram(filtered_df, x='rating', title="Rating Distribution")
st.plotly_chart(fig4)
