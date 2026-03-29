import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

st.title("📺 Netflix Analytics Dashboard")

# ---------- LOAD DATA ----------
df = pd.read_csv("netflix_titles.csv")

# ---------- SIDEBAR ----------
st.sidebar.header("Filters")

year = st.sidebar.selectbox(
    "Select Year",
    sorted(df['release_year'].unique())
)

country = st.sidebar.selectbox(
    "Select Country",
    df['country'].dropna().unique()
)

# ---------- GENRE FIX ----------
genres = df['listed_in'].str.split(',').explode().str.strip()
unique_genres = sorted(genres.dropna().unique())

genre = st.sidebar.selectbox(
    "Select Genre",
    unique_genres
)

content_type = st.sidebar.selectbox(
    "Type",
    df['type'].unique()
)

# ---------- FILTER DATA ----------
filtered_df = df[
    (df['release_year'] == year) &
    (df['country'] == country) &
    (df['type'] == content_type) &
    (df['listed_in'].str.contains(genre, case=False, na=False))
]

# ---------- KPIs ----------
st.subheader("📊 Overview")

col1, col2, col3 = st.columns(3)

col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

st.markdown("---")

# ---------- FILTERED DATA ----------
st.subheader("📄 Filtered Data")
st.dataframe(filtered_df)

st.markdown("---")

# ---------- MOVIES VS TV SHOWS PIE ----------
st.subheader("🎬 Movies vs TV Shows Distribution")

type_counts = df['type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']

fig = px.pie(
    type_counts,
    names='Type',
    values='Count'
)

st.plotly_chart(fig, use_container_width=True)
# ---------- TOP GENRES ----------
st.subheader("🎭 Top Genres")

genres_chart = df['listed_in'].str.split(',', expand=True).stack()
genre_counts = genres_chart.value_counts().head(10).reset_index()
genre_counts.columns = ['Genre', 'Count']

fig1 = px.bar(
    genre_counts,
    x='Genre',
    y='Count'
)

st.plotly_chart(fig1, use_container_width=True)

# ---------- TOP COUNTRIES ----------
st.subheader("🌍 Top Countries")

country_counts = df['country'].value_counts().head(10).reset_index()
country_counts.columns = ['Country', 'Count']

fig2 = px.bar(
    country_counts,
    x='Country',
    y='Count'
)

st.plotly_chart(fig2, use_container_width=True)

#------Content by Country-------

st.subheader("🌍 Content by Country")

country_counts = df['country'].value_counts().head(10).reset_index()
country_counts.columns = ['Country', 'Count']

fig = px.pie(country_counts, names='Country', values='Count')
st.plotly_chart(fig, use_container_width=True)

# ---------- RATINGS ----------
st.subheader("⭐ Ratings Distribution")

clean_df = df[~df['rating'].str.contains('min', case=False, na=False)]
rating_counts = clean_df['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']

fig3 = px.bar(
    rating_counts,
    x='Rating',
    y='Count'
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- CONTENT OVER TIME ----------
st.subheader("📈 Content Added Over Years")

year_counts = df['release_year'].value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']

fig6 = px.line(
    year_counts,
    x='Year',
    y='Count'
)
st.plotly_chart(fig6, use_container_width=True)
#--------Movies vs TV Shows Over Time--------

st.subheader("📈 Movies vs TV Shows Over Time")

trend = df.groupby(['release_year', 'type']).size().reset_index(name='Count')

fig = px.line(trend, x='release_year', y='Count', color='type')
st.plotly_chart(fig, use_container_width=True)
