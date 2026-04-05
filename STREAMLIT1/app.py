import streamlit as st
import pandas as pd
import plotly.express as px

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Netflix Master Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- PROFESSIONAL CSS (Netflix Theme) ----------
st.markdown("""
<style>
/* Main background */
.stApp {
    background-color: #141414;
    color: white;
}

/* Titles */
h1, h2, h3, h4 {
    color: #E50914; /* Netflix Red */
    font-weight: 600;
}

/* KPI Cards */
.card {
    background: #000000;
    padding: 18px;
    border: 2px solid #E50914;
    border-radius: 14px;
    text-align: center;
    box-shadow: 0px 6px 20px rgba(229, 9, 20, 0.15);
}
.card h2 { color: #ffffff; font-size: 40px; margin: 0; padding: 0; }
.card p { color: #aaaaaa; font-size: 16px; margin: 0; }

/* Section Container */
.section {
    background: #000000;
    padding: 20px;
    border: 1px solid #333333;
    border-radius: 16px;
    margin-bottom: 25px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background: #000000;
    border-right: 2px solid #333333;
}
</style>
""", unsafe_allow_html=True)

st.title("🎬 Netflix Content Intelligence Dashboard")

# ---------- LOAD & CLEAN DATA ----------
@st.cache_data
def load_data():
    # Use your local Excel file
    # This tells Python to look in the same folder where app.py is located
    df = pd.read_excel("netflix_data.xlsx")
    
    # Fill missing values to prevent errors in charts
    df['country'] = df['country'].fillna("Unknown")
    df['rating'] = df['rating'].fillna("Unknown")
    df['cast'] = df['cast'].fillna("Unknown")
    df['director'] = df['director'].fillna("Unknown")
    
    # Create a 'Primary Genre' for cleaner filtering
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0] if pd.notna(x) else 'Unknown')
    
    return df

df = load_data()

# ---------- SIDEBAR FILTERS ----------
st.sidebar.markdown("<h2 style='color: white;'>🎯 Filters</h2>", unsafe_allow_html=True)

# 1. Type Filter (Multiselect)
type_filter = st.sidebar.multiselect("Content Type", options=df['type'].unique(), default=df['type'].unique())

# 2. Year Filter (Slider)
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_filter = st.sidebar.slider("Release Year", min_year, max_year, (2010, max_year))

# 3. Country Filter (Multiselect - Top 20)
# Explode countries just for the filter list to keep it clean
top_countries = df['country'].str.split(', ').explode().value_counts().head(20).index.tolist()
if "Unknown" in top_countries: top_countries.remove("Unknown")
country_filter = st.sidebar.multiselect("Country", sorted(top_countries))

# 4. Genre Filter (Multiselect)
genre_filter = st.sidebar.multiselect("Genre", sorted(df['primary_genre'].unique()))

# ---------- APPLY FILTERS ----------
filtered_df = df[
    (df['type'].isin(type_filter)) &
    (df['release_year'].between(year_filter[0], year_filter[1]))
]

if country_filter:
    filtered_df = filtered_df[filtered_df['country'].str.contains('|'.join(country_filter))]

if genre_filter:
    filtered_df = filtered_df[filtered_df['primary_genre'].isin(genre_filter)]

# ---------- KPI METRICS ----------
st.markdown("### 📌 Key Metrics")
c1, c2, c3, c4 = st.columns(4)

# Calculate unique values
total_titles = len(filtered_df)
total_movies = len(filtered_df[filtered_df['type'] == 'Movie'])
total_tv = len(filtered_df[filtered_df['type'] == 'TV Show'])
# Get unique country count (handling the comma-separated strings)
total_countries = filtered_df['country'].str.split(', ').explode().nunique()

c1.markdown(f"<div class='card'><h2>{total_titles:,}</h2><p>Total Titles</p></div>", unsafe_allow_html=True)
c2.markdown(f"<div class='card'><h2>{total_movies:,}</h2><p>Movies</p></div>", unsafe_allow_html=True)
c3.markdown(f"<div class='card'><h2>{total_tv:,}</h2><p>TV Shows</p></div>", unsafe_allow_html=True)
c4.markdown(f"<div class='card'><h2>{total_countries:,}</h2><p>Producing Countries</p></div>", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ---------- SECTION 1: OVERVIEW ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Content Type Distribution")
    fig = px.pie(filtered_df, names='type', hole=0.6, color='type', 
                 color_discrete_map={'Movie': '#E50914', 'TV Show': '#ffffff'})
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Global Content Map")
    # Clean map data
    map_df = filtered_df['country'].str.split(', ').explode().value_counts().reset_index()
    map_df.columns = ['country', 'count']
    map_df = map_df[map_df['country'] != 'Unknown']
    
    fig = px.choropleth(map_df, locations='country', locationmode='country names', color='count',
                        color_continuous_scale='Reds')
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 2: GENRES & RATINGS ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top 10 Genres")
    g = filtered_df['primary_genre'].value_counts().head(10)
    fig = px.bar(g, x=g.values, y=g.index, orientation='h', color_discrete_sequence=['#E50914'])
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Ratings Distribution")
    r = filtered_df['rating'].value_counts()
    fig = px.bar(r, x=r.index, y=r.values, color_discrete_sequence=['#ffffff'])
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 3: TRENDS ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)
st.markdown("#### Content Trend Over Time")

trend = filtered_df.groupby(['release_year', 'type']).size().reset_index(name='count')
fig = px.line(trend, x='release_year', y='count', color='type', markers=True,
              color_discrete_map={'Movie': '#E50914', 'TV Show': '#ffffff'})
fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 4: DIRECTORS & ACTORS ----------
st.markdown("<div class='section'>", unsafe_allow_html=True)
col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Top 10 Directors")
    # Split and explode directors to get accurate counts
    d = filtered_df[filtered_df['director'] != 'Unknown']['director'].str.split(',').explode().str.strip().value_counts().head(10)
    fig = px.bar(d, x=d.index, y=d.values, color_discrete_sequence=['#E50914'])
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.markdown("#### Top 10 Actors")
    # Split and explode cast
    a = filtered_df[filtered_df['cast'] != 'Unknown']['cast'].str.split(',').explode().str.strip().value_counts().head(10)
    fig = px.bar(a, x=a.index, y=a.values, color_discrete_sequence=['#ffffff'])
    fig.update_layout(template='plotly_dark', plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
    st.plotly_chart(fig, use_container_width=True)

st.markdown("</div>", unsafe_allow_html=True)

# ---------- SECTION 5: DATA VIEWER ----------
st.markdown("### 🔎 Search & View Raw Data")
search_term = st.text_input("Search for a specific Movie, TV Show, Director, or Actor:")

if search_term:
    search_df = filtered_df[
        filtered_df['title'].str.contains(search_term, case=False, na=False) |
        filtered_df['director'].str.contains(search_term, case=False, na=False) |
        filtered_df['cast'].str.contains(search_term, case=False, na=False)
    ]
    st.dataframe(search_df[['title', 'type', 'release_year', 'director', 'cast', 'country', 'rating']])
elif st.checkbox("Show Raw Data Table"):
    st.dataframe(filtered_df[['title', 'type', 'release_year', 'director', 'cast', 'country', 'rating']].head(100))
