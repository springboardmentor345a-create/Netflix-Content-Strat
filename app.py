import streamlit as st
import pandas as pd
import plotly.express as px

# -----------------------------
# PAGE CONFIG
# -----------------------------
st.set_page_config(page_title="Netflix Dashboard", layout="wide")

# -----------------------------
# DARK THEME STYLE
# -----------------------------
st.markdown("""
    <style>
    body {
        background-color: #0f0f0f;
        color: white;
    }
    .stApp {
        background-color: #0f0f0f;
    }
    h1, h2, h3 {
        color: #E50914;
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------
# LOAD DATA
# -----------------------------
df = pd.read_csv("netflix_final_clean.csv", sep='\t', on_bad_lines='skip')

# Note: Keep Unknown values in the base dataset for accurate totals
# Only filter them out in specific visualizations

# -----------------------------
# SIDEBAR NAVIGATION
# -----------------------------
st.sidebar.title("📊 Navigation")

page = st.sidebar.radio("Go to", [
    "Overview",
    "Content Analysis",
    "Genre & Ratings",
    "Trend & Time"
])

# -----------------------------
# FILTERS
# -----------------------------
st.sidebar.header("Filters")

year = st.sidebar.multiselect("Year", sorted(df["year_added"].dropna().unique()))
genre = st.sidebar.multiselect("Genre", sorted(df[df["primary_genre"]!="Unknown"]["primary_genre"].unique()))
country = st.sidebar.multiselect("Country", sorted(df[df["primary_country"]!="Unknown"]["primary_country"].unique()))
ctype = st.sidebar.multiselect("Type", df["type"].unique())

# Apply filters
filtered_df = df.copy()

if year:
    filtered_df = filtered_df[filtered_df["year_added"].isin(year)]
if genre:
    filtered_df = filtered_df[filtered_df["primary_genre"].isin(genre)]
if country:
    filtered_df = filtered_df[filtered_df["primary_country"].isin(country)]
if ctype:
    filtered_df = filtered_df[filtered_df["type"].isin(ctype)]

# -----------------------------
# PAGE 1: OVERVIEW
# -----------------------------
if page == "Overview":
    st.title("🎬 Netflix Overview Dashboard")

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Shows", len(df))
    col2.metric("Total Genres", df["primary_genre"].nunique())
    col3.metric("Total Countries", df["primary_country"].nunique())
    col4.metric("Total Ratings", df["rating"].nunique())

    st.subheader("Top Genres Over Years")
    genre_year = filtered_df[(filtered_df["primary_genre"]!="Unknown") & (filtered_df["year_added"] > 2000) & (filtered_df["year_added"].notna())].groupby(["year_added", "primary_genre"]).size().reset_index(name="count")
    genre_year["year_added"] = genre_year["year_added"].astype(int)
    fig = px.bar(genre_year, x="year_added", y="count", color="primary_genre")
    st.plotly_chart(fig, use_container_width=True, key="genres_years")

    st.subheader("Country Analysis")
    country_counts = filtered_df[filtered_df["primary_country"]!="Unknown"]["primary_country"].value_counts().head(10).reset_index()
    country_counts.columns = ["country", "count"]
    fig = px.bar(country_counts, y="country", x="count", orientation='h', color_discrete_sequence=['#E50914'])
    st.plotly_chart(fig, use_container_width=True, key="country_analysis")

    st.subheader("Ratings Distribution")
    rating_counts = filtered_df[filtered_df["rating"]!="Unknown"]["rating"].value_counts()
    fig = px.pie(values=rating_counts.values, names=rating_counts.index)
    st.plotly_chart(fig, use_container_width=True, key="ratings_dist_overview")

    st.subheader("Content Trend")
    trend = filtered_df[(filtered_df["year_added"] > 2000) & (filtered_df["year_added"].notna())].groupby("year_added").size().reset_index(name="count")
    trend["year_added"] = trend["year_added"].astype(int)
    fig = px.line(trend, x="year_added", y="count", color_discrete_sequence=['#E50914'])
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True, key="content_trend_overview")

# -----------------------------
# PAGE 2: CONTENT ANALYSIS
# -----------------------------
elif page == "Content Analysis":
    st.title("🎬 Content Analysis")

    col1, col2 = st.columns(2)
    col1.metric("Movies", len(df[df["type"]=="Movie"]))
    col2.metric("TV Shows", len(df[df["type"]=="Tv Show"]))

    st.subheader("Movies vs TV Shows")
    type_counts = filtered_df["type"].value_counts()
    fig = px.pie(values=type_counts.values, names=type_counts.index)
    st.plotly_chart(fig, use_container_width=True, key="movies_vs_tv")

    st.subheader("Top Countries")
    country_data = filtered_df[filtered_df["primary_country"]!="Unknown"]["primary_country"].value_counts().head(15).reset_index()
    country_data.columns = ["country", "count"]
    fig = px.scatter_geo(country_data, locations="country",
                         locationmode="country names", size="count", hover_name="country")
    st.plotly_chart(fig, use_container_width=True, key="top_countries")

    st.subheader("Top Directors")
    directors = filtered_df[filtered_df["director"]!="Unknown"]["director"].value_counts().head(10).reset_index()
    directors.columns = ["director", "count"]
    fig = px.bar(directors, y="director", x="count", orientation='h', color_discrete_sequence=['#E50914'])
    fig.update_layout(yaxis_title="Director", xaxis_title="Count")
    st.plotly_chart(fig, use_container_width=True, key="top_directors")

# -----------------------------
# PAGE 3: GENRE & RATINGS
# -----------------------------
elif page == "Genre & Ratings":
    st.title("🎬 Genre & Rating Insights")

    st.subheader("Genre Distribution")
    genre_counts = filtered_df[filtered_df["primary_genre"]!="Unknown"]["primary_genre"].value_counts().head(10)
    fig = px.pie(values=genre_counts.values, names=genre_counts.index)
    st.plotly_chart(fig, use_container_width=True, key="genre_dist")

    st.subheader("Ratings Distribution")
    rating_counts = filtered_df[filtered_df["rating"]!="Unknown"]["rating"].value_counts().reset_index()
    rating_counts.columns = ["rating", "count"]
    fig = px.bar(rating_counts, x="rating", y="count", color_discrete_sequence=['#E50914'])
    st.plotly_chart(fig, use_container_width=True, key="ratings_dist")

    st.subheader("Genre vs Rating")
    matrix = pd.crosstab(filtered_df[filtered_df["primary_genre"]!="Unknown"]["primary_genre"], 
                         filtered_df[filtered_df["rating"]!="Unknown"]["rating"])
    st.dataframe(matrix)

# -----------------------------
# PAGE 4: TREND ANALYSIS
# -----------------------------
elif page == "Trend & Time":
    st.title("🎬 Trend & Time Analysis")

    st.subheader("Content Growth Over Time")
    trend = filtered_df[(filtered_df["year_added"] > 2000) & (filtered_df["year_added"].notna())].groupby("year_added").size().reset_index(name="count")
    trend["year_added"] = trend["year_added"].astype(int)
    fig = px.line(trend, x="year_added", y="count", color_discrete_sequence=['#E50914'])
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True, key="content_growth")

    st.subheader("Movies vs TV Trend")
    trend_type = filtered_df[(filtered_df["year_added"] > 2000) & (filtered_df["year_added"].notna())].groupby(["year_added", "type"]).size().reset_index(name="count")
    trend_type["year_added"] = trend_type["year_added"].astype(int)
    fig = px.line(trend_type, x="year_added", y="count", color="type")
    fig.update_traces(line=dict(width=3))
    st.plotly_chart(fig, use_container_width=True, key="movies_vs_tv_trend")

    st.subheader("Top Genre Trends (Top 5)")
    top_genres = filtered_df[filtered_df["primary_genre"]!="Unknown"]["primary_genre"].value_counts().head(5).index
    df_top = filtered_df[(filtered_df["primary_genre"].isin(top_genres)) & (filtered_df["year_added"] > 2000) & (filtered_df["year_added"].notna())]
    trend_genre = df_top.groupby(["year_added", "primary_genre"]).size().reset_index(name="count")
    trend_genre["year_added"] = trend_genre["year_added"].astype(int)
    fig = px.area(trend_genre, x="year_added", y="count", color="primary_genre")
    st.plotly_chart(fig, use_container_width=True, key="genre_trends")