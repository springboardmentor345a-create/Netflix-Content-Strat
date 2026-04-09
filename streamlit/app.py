import streamlit as st
import pandas as pd
import plotly.express as px
import requests, io

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Streaming Analytics Dashboard",
    layout="wide"
)

# ---------- PROFESSIONAL CSS ----------
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #0B132B;
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #6FFFE9;
    font-weight: 600;
}

/* KPI Cards */
.card {
    background: #1C2541;
    padding: 18px;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.4);
}

/* Section Container */
.section {
    background: #1C2541;
    padding: 20px;
    border-radius: 16px;
    margin-bottom: 20px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #111827;
}

</style>
""", unsafe_allow_html=True)

st.title("📊 Streaming Content Intelligence Dashboard")

# ---------- LOAD DATA ----------
@st.cache_data
def load_data():
    url = 'https://drive.google.com/uc?export=download&id=1uCSB6lS329wnOLrQCKHOj3ZxWYM6MGX-'
    df = pd.read_csv(io.StringIO(requests.get(url).content.decode('utf-8')))
    
    df['country'] = df['country'].fillna("Unknown")
    df['rating'] = df['rating'].fillna("Unknown")
    df['cast'] = df['cast'].fillna("Unknown")
    df['director'] = df['director'].fillna("Unknown")
    
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0] if pd.notna(x) else 'Unknown')
    
    return df

df = load_data()

# ---------- SIDEBAR ----------
st.sidebar.header("Filters")

type_filter = st.sidebar.multiselect("Content Type", df['type'].unique(), default=df['type'].unique())

year_filter = st.sidebar.slider(
    "Release Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2015, 2021)
)

country_filter = st.sidebar.multiselect("Country", df['country'].value_counts().head(15).index)

genre_filter = st.sidebar.multiselect("Genre", sorted(df['primary_genre'].unique()))

# ---------- FILTER ----------
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_filter[0], year_filter[1]))
]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].str.contains('|'.join(country_filter))]

if genre_filter:
    filtered_df = filtered_df[filtered_df['primary_genre'].isin(genre_filter)]

# ---------- KPI ----------
st.markdown("### 📌 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='card'><h2>{len(filtered_df)}</h2><p>Total Titles</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h2>{len(filtered_df[filtered_df['type']=='Movie'])}</h2><p>Movies</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h2>{len(filtered_df[filtered_df['type']=='TV Show'])}</h2><p>TV Shows</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h2>{filtered_df['country'].nunique()}</h2><p>Countries</p></div>", unsafe_allow_html=True)

# ---------- SECTION 1 ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Content Type Distribution")
    fig = px.pie(filtered_df, names='type', hole=0.6,
                 color_discrete_sequence=['#5BC0BE','#9A8CFF'])
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Global Content Map")
    map_df = filtered_df['country'].value_counts().reset_index()
    map_df.columns = ['country','count']
    fig = px.choropleth(map_df, locations='country',
                        locationmode='country names',
                        color='count',
                        color_continuous_scale='Teal')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 2 ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Genres")
    g = filtered_df['primary_genre'].value_counts().head(10)
    fig = px.bar(g, x=g.index, y=g.values,
                 color=g.values,
                 color_continuous_scale='Teal')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Ratings Distribution")
    r = filtered_df['rating'].value_counts()
    fig = px.bar(r, x=r.index, y=r.values,
                 color=r.values,
                 color_continuous_scale='Purples')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 3 ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)

st.subheader("Content Trend Over Time")

trend = filtered_df.groupby(['release_year','type']).size().reset_index(name='count')

fig = px.line(trend, x='release_year', y='count',
              color='type',
              markers=True,
              color_discrete_sequence=['#5BC0BE','#9A8CFF'])

fig.update_layout(template='plotly_dark')

st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 4 ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Directors")
    d = filtered_df['director'].str.split(',').explode().str.strip().value_counts().head(10)
    fig = px.bar(d, x=d.index, y=d.values, color=d.values,
                 color_continuous_scale='Teal')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.subheader("Top Actors")
    a = filtered_df['cast'].str.split(',').explode().str.strip().value_counts().head(10)
    fig = px.bar(a, x=a.index, y=a.values, color=a.values,
                 color_continuous_scale='Purples')
    fig.update_layout(template='plotly_dark')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- DATA ----------
if st.checkbox("Show Data"):
    st.dataframe(filtered_df)
