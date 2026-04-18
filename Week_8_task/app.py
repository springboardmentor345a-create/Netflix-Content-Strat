import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# ---------------- CSS STYLING ----------------
st.markdown("""
<style>

/* Background */
.stApp {
    background-color: #0B0C10;
    color: white;
}

/* Titles */
h1, h2, h3 {
    color: #E50914;
}

/* KPI Cards */
.card {
    background: #111111;
    padding: 20px;
    border-radius: 12px;
    border-left: 6px solid #E50914;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(0,0,0,0.5);
}

/* KPI Text */
.card p {
    color: #aaaaaa;
}

/* Section Box */
.section {
    background: #111111;
    padding: 20px;
    border-radius: 15px;
    margin-bottom: 20px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #111111;
}

</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("netflix_cleaned.csv")

df['country'] = df['country'].fillna("Unknown")
df['rating'] = df['rating'].fillna("Unknown")

df['primary_genre'] = df['listed_in'].apply(
    lambda x: x.split(',')[0] if pd.notna(x) else "Unknown"
)

# FIX YEAR
df['release_year'] = pd.to_datetime(df['release_year'], errors='coerce').dt.year
df = df.dropna(subset=['release_year'])
df['release_year'] = df['release_year'].astype(int)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎯 Filters")

type_filter = st.sidebar.multiselect("Type", df['type'].unique(), default=df['type'].unique())
country_filter = st.sidebar.multiselect("Country", df['country'].unique())

year_filter = st.sidebar.slider(
    "Year",
    int(df['release_year'].min()),
    int(df['release_year'].max()),
    (2000, 2021)
)

# ---------------- FILTER ----------------
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_filter[0], year_filter[1]))
]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].isin(country_filter)]

# ---------------- TITLE ----------------
st.title("🎬 Netflix Analytics Dashboard")

# ---------------- KPI SECTION ----------------
st.markdown("### 📊 Key Metrics")

c1, c2, c3, c4 = st.columns(4)

c1.markdown(f"<div class='card'><h2>{len(filtered_df)}</h2><p>Total Titles</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h2>{len(filtered_df[filtered_df['type']=='Movie'])}</h2><p>Movies</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h2>{len(filtered_df[filtered_df['type']=='Tv Show'])}</h2><p>TV Shows</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h2>{filtered_df['country'].nunique()}</h2><p>Countries</p></div>", unsafe_allow_html=True)

# ---------------- SECTION 1 ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### 📊 Content Analysis")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Top Genres")
    genre_counts = filtered_df['primary_genre'].value_counts().head(10)

    fig1 = px.bar(
        genre_counts,
        x=genre_counts.values,
        y=genre_counts.index,
        orientation='h',
        color=genre_counts.values,
        color_continuous_scale='Reds'
    )
    fig1.update_layout(template='plotly_dark')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Content Type Distribution")

    fig2 = px.pie(
        filtered_df,
        names='type',
        hole=0.5,
        color_discrete_sequence=['#E50914', '#ffffff']
    )
    fig2.update_layout(template='plotly_dark')
    st.plotly_chart(fig2, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SECTION 2 ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### 🌍 Country Analysis")

country_counts = filtered_df['country'].value_counts().head(10)

fig3 = px.bar(
    country_counts,
    x=country_counts.index,
    y=country_counts.values,
    color=country_counts.values,
    color_continuous_scale='Reds'
)

fig3.update_layout(template='plotly_dark')
st.plotly_chart(fig3, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SECTION 3 ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### ⭐ Ratings Analysis")

rating_counts = filtered_df['rating'].value_counts()

fig4 = px.bar(
    rating_counts,
    x=rating_counts.index,
    y=rating_counts.values,
    color=rating_counts.values,
    color_continuous_scale='Reds'
)

fig4.update_layout(template='plotly_dark')
st.plotly_chart(fig4, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------------- SECTION 4 ----------------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("### 📈 Content Growth Over Time")

trend = filtered_df.groupby('release_year').size().reset_index(name='count')

fig5 = px.line(
    trend,
    x='release_year',
    y='count',
    markers=True
)

fig5.update_layout(template='plotly_dark')
st.plotly_chart(fig5, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)