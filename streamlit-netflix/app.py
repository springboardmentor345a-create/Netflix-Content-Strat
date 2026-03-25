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

# ---------- TOP GENRES ----------
st.subheader("🎭 Top Genres")

genres_chart = df['listed_in'].str.split(',', expand=True).stack()
genre_counts = genres_chart.value_counts().head(10).reset_index()
genre_counts.columns = ['Genre', 'Count']

fig1 = px.bar(
    genre_counts,
    x='Genre',
    y='Count',
    color_discrete_sequence=['#E50914']
)

st.plotly_chart(fig1, use_container_width=True)

# ---------- TOP COUNTRIES ----------
st.subheader("🌍 Top Countries")

country_counts = df['country'].value_counts().head(10).reset_index()
country_counts.columns = ['Country', 'Count']

fig2 = px.bar(
    country_counts,
    x='Country',
    y='Count',
    color_discrete_sequence=['#E50914']
)

st.plotly_chart(fig2, use_container_width=True)

# ---------- RATINGS ----------
st.subheader("⭐ Ratings Distribution")

clean_df = df[~df['rating'].str.contains('min', case=False, na=False)]
rating_counts = clean_df['rating'].value_counts().reset_index()
rating_counts.columns = ['Rating', 'Count']

fig3 = px.bar(
    rating_counts,
    x='Rating',
    y='Count',
    color_discrete_sequence=['#E50914']
)

st.plotly_chart(fig3, use_container_width=True)

# ---------- TOP GENRES PER YEAR ----------
st.subheader("📅 Top Genres (Selected Year)")

year_df = df[df['release_year'] == year]
year_genres = year_df['listed_in'].str.split(',').explode().str.strip()

year_genre_counts = year_genres.value_counts().head(10).reset_index()
year_genre_counts.columns = ['Genre', 'Count']

fig4 = px.bar(
    year_genre_counts,
    x='Genre',
    y='Count',
    color_discrete_sequence=['#E50914']
)

st.plotly_chart(fig4, use_container_width=True)

# ---------- CONTENT TYPE BY COUNTRY ----------
st.subheader("🎬 Content Type in Selected Country")

country_df = df[df['country'] == country]
type_counts = country_df['type'].value_counts().reset_index()
type_counts.columns = ['Type', 'Count']

fig5 = px.bar(
    type_counts,
    x='Type',
    y='Count',
    color_discrete_sequence=['#E50914']
)

st.plotly_chart(fig5, use_container_width=True)

# ---------- CONTENT OVER TIME ----------
st.subheader("📈 Content Added Over Years")

year_counts = df['release_year'].value_counts().sort_index().reset_index()
year_counts.columns = ['Year', 'Count']

fig6 = px.line(
    year_counts,
    x='Year',
    y='Count'
)

fig6.update_traces(line=dict(color='#E50914'))

st.plotly_chart(fig6, use_container_width=True)
