import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.io as pio
from theme import apply_netflix_theme

# ---------------------------
# SETTINGS & THEME
# ---------------------------
pio.templates.default = "plotly_dark"
st.set_page_config(page_title="Netflix Dashboard", layout="wide")
apply_netflix_theme()

# Helper to ensure all charts have black background and white text
def style_chart(fig):
    fig.update_layout(
        plot_bgcolor="rgba(0,0,0,0)",
        paper_bgcolor="rgba(0,0,0,0)",
        font=dict(color="white"),
        title_font=dict(color="white", size=20),
        legend_font=dict(color="white"),
        xaxis=dict(gridcolor='#333333', tickfont=dict(color='white')),
        yaxis=dict(gridcolor='#333333', tickfont=dict(color='white'))
    )
    return fig

# Standard Color Map for consistency
color_map = {
    'Movie': '#E50914',       # Netflix Red
    'TV Show': '#FFFFFF',    # White
    'Licensed': '#E50914', 
    'Netflix Original': '#FFFFFF'
}

# ---------------------------
# LOAD DATA
# ---------------------------
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_final.csv")
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year
    df['duration_num'] = df['duration'].str.extract(r'(\d+)').astype(float)
    df['content_origin'] = df['content_origin'].str.strip()
    return df

df = load_data()

# ---------------------------
# SIDEBAR FILTERS
# ---------------------------
st.sidebar.title("Filters")
year = st.sidebar.selectbox("Select Year", ["All"] + sorted(df['year_added'].dropna().unique().astype(int).tolist()))
type_filter = st.sidebar.multiselect("Select Type", df['type'].unique(), default=df['type'].unique())

filtered_df = df.copy()
if year != "All":
    filtered_df = filtered_df[filtered_df['year_added'] == year]
if type_filter:
    filtered_df = filtered_df[filtered_df['type'].isin(type_filter)]

page = st.sidebar.radio("Navigation", ["Overview", "Content Analysis", "Country Distribution", "Genre + Conclusion"])

# ===========================
# 🏠 PAGE 1: OVERVIEW
# ===========================
if page == "Overview":
    st.title("🎬 Netflix Dashboard Overview")

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Titles", filtered_df['show_id'].nunique())
    col2.metric("Movies", filtered_df[filtered_df['type']=="Movie"]['show_id'].nunique())
    col3.metric("TV Shows", filtered_df[filtered_df['type']=="TV Show"]['show_id'].nunique())

    col4, col5 = st.columns(2)
    col4.metric("Licensed", filtered_df[filtered_df['content_origin']=="Licensed"]['show_id'].nunique())
    col5.metric("Netflix Originals", filtered_df[filtered_df['content_origin']=="Netflix Original"]['show_id'].nunique())

    # Pie Chart
    fig = px.pie(filtered_df, names='type', color='type', 
                 color_discrete_map=color_map, title="Content Type Distribution")
    st.plotly_chart(style_chart(fig), use_container_width=True)

    # Trend Line
    trend = filtered_df.groupby('year_added')['show_id'].count().reset_index()
    fig2 = px.line(trend, x='year_added', y='show_id', title="Content Trend Over Years")
    fig2.update_traces(line_color='#E50914')
    st.plotly_chart(style_chart(fig2), use_container_width=True)

    st.info("⚠️ Note: Trend reflects dataset availability, not actual Netflix decline.")

# ===========================
# 📊 PAGE 2: CONTENT ANALYSIS
# ===========================
elif page == "Content Analysis":
    st.title("📊 Content Analysis")
    col1, col2 = st.columns(2)

    # Bar Chart: Rating
    rating_dist = filtered_df['rating'].value_counts().reset_index()
    fig = px.bar(rating_dist, x='rating', y='count', title="Rating Distribution", color_discrete_sequence=['#E50914'])
    col1.plotly_chart(style_chart(fig), use_container_width=True)

    # Histogram: Rating vs Type
    fig2 = px.histogram(filtered_df, x='rating', color='type', barmode='group', 
                        title="Rating vs Type", color_discrete_map=color_map)
    col2.plotly_chart(style_chart(fig2), use_container_width=True)

    # Histogram: Duration
    fig3 = px.histogram(filtered_df[filtered_df['duration_num'] > 0], x='duration_num', nbins=30, 
                        title="Duration Distribution", color_discrete_sequence=['#E50914'])
    st.plotly_chart(style_chart(fig3), use_container_width=True)
    st.success("👉 TV-MA dominates, indicating mature audience")

# ===========================
# 🌍 PAGE 3: COUNTRY
# ===========================
elif page == "Country Distribution":
    st.title("🌍 Country Distribution")

    df_country = filtered_df.copy()
    df_country['country'] = df_country['country'].str.split(',').explode('country').str.strip()
    
    country_count = df_country['country'].value_counts().reset_index()
    country_count.columns = ['country', 'count']

    # Choropleth Map
    fig = px.choropleth(country_count, locations='country', locationmode='country names', 
                        color='count', title="Content by Country", color_continuous_scale=['#440000', '#E50914', '#FFFFFF'])
    st.plotly_chart(style_chart(fig), use_container_width=True)

    # Top Countries Bar
    fig2 = px.bar(country_count.head(10), x='country', y='count', title="Top Countries", color_discrete_sequence=['#E50914'])
    st.plotly_chart(style_chart(fig2), use_container_width=True)
    
    st.subheader("📊 Licensed vs Netflix Originals")
    col1, col2 = st.columns(2)

    origin_count = filtered_df['content_origin'].value_counts().reset_index()
    origin_count.columns = ['origin', 'count']

    # Donut Chart
    fig_origin = px.pie(origin_count, names='origin', values='count', hole=0.5, 
                        title="Content Origin Split", color='origin', color_discrete_map=color_map)
    col1.plotly_chart(style_chart(fig_origin), use_container_width=True)

    # Origin Bar
    fig_origin_bar = px.bar(origin_count, x='origin', y='count', color='origin', 
                            title="Licensed vs Originals", color_discrete_map=color_map)
    col2.plotly_chart(style_chart(fig_origin_bar), use_container_width=True)

    # Country vs Type
    top_countries = df_country['country'].value_counts().nlargest(8).index
    filtered_country_df = df_country[df_country['country'].isin(top_countries)]
    country_type = filtered_country_df.groupby(['country', 'type']).size().reset_index(name='count')

    fig3 = px.bar(country_type, x='count', y='country', color='type', orientation='h', 
                 barmode='group', title="Country vs Type", color_discrete_map=color_map)
    st.plotly_chart(style_chart(fig3), use_container_width=True)

# ===========================
# 🎭 PAGE 4: GENRE + CONCLUSION
# ===========================
elif page == "Genre + Conclusion":
    st.title("🎭 Genre Insights & Conclusion")

    df_genre = filtered_df.copy()
    df_genre['listed_in'] = df_genre['listed_in'].str.split(',').explode('listed_in').str.strip()

    top_genre = df_genre['listed_in'].value_counts().reset_index().head(7)
    top_genre.columns = ['genre', 'count']

    # Genre Bar
    fig = px.bar(top_genre, x='count', y='genre', orientation='h', title="Top Genres", color_discrete_sequence=['#E50914'])
    st.plotly_chart(style_chart(fig), use_container_width=True)

    # Genre vs Type
    top_genres_list = top_genre['genre'].tolist()
    filtered_genre_df = df_genre[df_genre['listed_in'].isin(top_genres_list)]
    fig2 = px.histogram(filtered_genre_df, x='listed_in', color='type', barmode='group',
                        title="Genre vs Type", color_discrete_map=color_map)
    color_discrete_map={
        'Movie': '#E50914', 
        'TV Show': '#FFFFFF'
    }
    st.plotly_chart(style_chart(fig2), use_container_width=True)

    # Genre vs Origin
    origin_genre = filtered_genre_df.groupby(['listed_in', 'content_origin']).size().reset_index(name='count')
    fig_origin_genre = px.bar(origin_genre, x='listed_in', y='count', color='content_origin', 
                               title="Genre vs Content Origin", color_discrete_map=color_map)
    st.plotly_chart(style_chart(fig_origin_genre), use_container_width=True)

    st.subheader("🧠 Key Insights")
    st.markdown("""
    <div style="font-size:20px; line-height:1.8; background-color:#111111; padding:20px; border-radius:10px; border-left: 5px solid #E50914; color:white;">
    • Content increased after 2015 <br>
    • Movies dominate (~70%) <br>
    • USA leads content <br>
    • TV-MA most common <br>
    • Licensed > Originals  
    </div>
    """, unsafe_allow_html=True)