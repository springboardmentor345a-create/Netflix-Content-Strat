import streamlit as st
import pandas as pd
import plotly.express as px

# ------------------ PAGE CONFIG ------------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# ------------------ NETFLIX THEME ------------------
st.markdown("""
<style>

/* Background */
html, body, [class*="css"] {
    background-color: #141414 !important;
}

/* Main */
[data-testid="stAppViewContainer"],
section[data-testid="stMain"],
.block-container,
header {
    background-color: #141414 !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #000000 !important;
}

/* Sidebar inputs */
section[data-testid="stSidebar"] .stSelectbox,
section[data-testid="stSidebar"] .stSlider {
    background-color: #1f1f1f !important;
    border-radius: 8px;
    padding: 5px;
}

/* Fix dropdown */
div[data-baseweb="select"] > div {
    background-color: #1f1f1f !important;
    color: white !important;
}

div[data-baseweb="menu"] {
    background-color: #1f1f1f !important;
    color: white !important;
}

div[data-baseweb="menu"] div:hover {
    background-color: #E50914 !important;
}

/* Text */
h1, h2, h3, h4, h5, h6, p, span, div {
    color: white !important;
}

/* Table */
[data-testid="stDataFrame"] {
    background-color: #1f1f1f !important;
    border-radius: 10px;
}

/* 🔥 FULL DROPDOWN FIX (FINAL) */

/* Dropdown popup container */
div[data-baseweb="popover"] > div {
    background-color: #1f1f1f !important;
}

/* Dropdown menu */
ul[role="listbox"] {
    background-color: #1f1f1f !important;
}

/* Each option */
li[role="option"] {
    background-color: #1f1f1f !important;
    color: white !important;
}

/* Hover */
li[role="option"]:hover {
    background-color: #E50914 !important;
    color: white !important;
}

/* Selected option */
li[aria-selected="true"] {
    background-color: #E50914 !important;
    color: white !important;
}

/* DARK TABLE FIX */
[data-testid="stDataFrame"] table {
    background-color: #1f1f1f !important;
    color: white !important;
}

[data-testid="stDataFrame"] th {
    background-color: #000000 !important;
    color: #E50914 !important;
}

[data-testid="stDataFrame"] td {
    background-color: #1f1f1f !important;
    color: white !important;
}

</style>
""", unsafe_allow_html=True)

# ------------------ LOAD DATA ------------------
df = pd.read_csv("netflix_final.csv")

# ------------------ HEADER ------------------
st.markdown("""
<h1 style='color:#E50914;'>🎬 Netflix Analytics Dashboard</h1>
<p style='color:gray;'>Insights from Netflix Dataset</p>
""", unsafe_allow_html=True)

# ------------------ PREPROCESS ------------------
df['country'] = df['country'].fillna("Unknown")
df['listed_in'] = df['listed_in'].fillna("Unknown")

# Genres
genre_series = df['listed_in'].str.split(', ')
all_genres = sorted(set([g for sub in genre_series for g in sub]))

# Countries
country_series = df['country'].str.split(', ')
all_countries = sorted(set([c for sub in country_series for c in sub]))

# ------------------ SIDEBAR FILTERS ------------------
st.sidebar.header("Filters")

# ✅ FIXED YEAR FILTER (IMPORTANT CHANGE)
year_options = ["All"] + sorted(df['release_year'].unique())
year = st.sidebar.selectbox("Select Year", year_options)

type_filter = st.sidebar.selectbox(
    "Select Type",
    ["All"] + list(df['type'].dropna().unique())
)

genre_filter = st.sidebar.selectbox(
    "Select Genre",
    ["All"] + all_genres
)

country_filter = st.sidebar.selectbox(
    "Select Country",
    ["All"] + all_countries
)

# ------------------ FILTERING (FIXED LOGIC) ------------------
filtered_df = df.copy()

if year != "All":
    filtered_df = filtered_df[filtered_df['release_year'] == year]

if type_filter != "All":
    filtered_df = filtered_df[filtered_df['type'] == type_filter]

if genre_filter != "All":
    filtered_df = filtered_df[
        filtered_df['listed_in'].str.contains(genre_filter, na=False)
    ]

if country_filter != "All":
    filtered_df = filtered_df[
        filtered_df['country'].str.contains(country_filter, na=False)
    ]

# ------------------ KPI CARDS ------------------
st.markdown("### 📊 Key Metrics")

col1, col2, col3 = st.columns(3)

def kpi_card(title, value):
    st.markdown(f"""
    <div style="
        background-color:#1f1f1f;
        padding:25px;
        border-radius:15px;
        text-align:center;
        box-shadow: 0px 0px 15px rgba(229,9,20,0.2);
    ">
        <h4 style='color:gray'>{title}</h4>
        <h1 style='color:#E50914'>{value}</h1>
    </div>
    """, unsafe_allow_html=True)

with col1:
    kpi_card("Total Titles", len(df))

with col2:
    kpi_card("Movies", len(df[df['type'].str.contains("Movie", case=False, na=False)]))

with col3:
    kpi_card("TV Shows", len(df[df['type'].str.contains("TV", case=False, na=False)]))
    
#st.markdown(f"<p style='color:gray;'>Showing {len(filtered_df)} of {len(df)} titles</p>", unsafe_allow_html=True)

#st.markdown("<br>", unsafe_allow_html=True)

#"Displaying {len(filtered_df)} results out of {len(df)} total titles"

st.markdown("<hr style='border:1px solid #333;'>", unsafe_allow_html=True)

if filtered_df.empty:
    st.warning("No data available for selected filters")

# ------------------ CHARTS ------------------
col1, col2 = st.columns(2)

# Top Genres
with col1:
    st.markdown("### 🎭 Top Genres")
    g_series = filtered_df['listed_in'].str.split(', ')
    g_series = pd.Series([g for sub in g_series for g in sub])
    top_genres = g_series.value_counts().head(8)

    fig = px.bar(x=top_genres.index, y=top_genres.values,
                 color_discrete_sequence=["#E50914"])
    fig.update_layout(
    plot_bgcolor="#1f1f1f",
    paper_bgcolor="#141414",
    font_color="white",
    margin=dict(l=40, r=40, t=40, b=40),
    xaxis=dict(showgrid=False),
    yaxis=dict(gridcolor="#444")
    )
    st.plotly_chart(fig, use_container_width=True)

# Country Distribution
with col2:
    st.markdown("### 🌍 Content by Country")
    c_series = filtered_df['country'].str.split(', ')
    c_series = pd.Series([c for sub in c_series for c in sub])
    top_countries = c_series.value_counts().head(8)

    fig = px.bar(x=top_countries.index, y=top_countries.values,
                 color_discrete_sequence=["#E50914"])
    fig.update_layout(
        plot_bgcolor="#1f1f1f",
        paper_bgcolor="#141414",
        font_color="white"
    )
    st.plotly_chart(fig, use_container_width=True)

# Rating Distribution
st.markdown("### ⭐ Rating Distribution")
rating_dist = filtered_df['rating'].value_counts()

fig = px.bar(x=rating_dist.index, y=rating_dist.values,
             color_discrete_sequence=["#E50914"])
fig.update_layout(
    plot_bgcolor="#1f1f1f",
    paper_bgcolor="#141414",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)

# Trend
st.markdown("### 📈 Content Trend Over Years")
trend = df.groupby('release_year').size()

fig = px.line(x=trend.index, y=trend.values)
fig.update_traces(line_color="#E50914")
fig.update_layout(
    plot_bgcolor="#1f1f1f",
    paper_bgcolor="#141414",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)

# ------------------ TABLE ------------------
st.markdown("### 📋 Filtered Data Preview")
st.dataframe(filtered_df.head(15))

