import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import numpy as np

# 1. Page Configuration
st.set_page_config(page_title="Netflix Content Dashboard", layout="wide")
st.title("🎬 Netflix Content Analysis Dashboard")
st.markdown("Analyze Netflix's catalog, exploring content types, global distribution, genres, and growth trends.")

# 2. Data Loading & Preprocessing
@st.cache_data # Cache the data to improve load times
def load_data():
    # Replace with your actual dataset filename if different
    df = pd.read_csv("Week-5-task/netflix_titles (1).csv")
    
    # Clean data (handling nulls)
    df['country'] = df['country'].fillna('Unknown')
    df['rating'] = df['rating'].fillna('Unknown')
    df['director'] = df['director'].fillna('Unknown')
    df['cast'] = df['cast'].fillna('Unknown')
    
    # Ensure release_year is integer
    df['release_year'] = df['release_year'].astype(int)
    
    # Process genres (listed_in) to handle multiple genres per row for filtering
    df['primary_genre'] = df['listed_in'].apply(lambda x: x.split(',')[0] if pd.notna(x) else 'Unknown')
    
    # Additional processing for growth analysis
    df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
    df['year_added'] = df['date_added'].dt.year.fillna(0).astype(int)
    
    return df

@st.cache_data
def prepare_clustering_data(df):
    # Create a copy for clustering
    df_clustering = df.copy()
    
    # Process duration
    df_clustering['duration_value'] = df_clustering['duration'].str.extract(r'(\d+)').astype(float)
    df_clustering['duration_normalized'] = df_clustering['duration_value'].copy()
    df_clustering.loc[df_clustering['type'] == 'TV Show', 'duration_normalized'] = \
        df_clustering.loc[df_clustering['type'] == 'TV Show', 'duration_normalized'].clip(upper=15)
    df_clustering.loc[df_clustering['type'] == 'Movie', 'duration_normalized'] = \
        df_clustering.loc[df_clustering['type'] == 'Movie', 'duration_normalized'].clip(upper=200)
    
    # Rating to numeric
    rating_map = {
        'G': 1, 'TV-Y': 1, 'TV-Y7': 2, 'TV-Y7-FV': 2, 'PG': 3, 'TV-PG': 3,
        'PG-13': 4, 'TV-14': 4, 'R': 5, 'TV-MA': 5, 'NC-17': 6, 'UR': 3, 'Unknown': 3
    }
    df_clustering['rating_numeric'] = df_clustering['rating'].map(rating_map).fillna(3)
    
    # Genre encoding (top 20 genres)
    all_genres = df_clustering['listed_in'].str.split(', ').explode().str.strip().unique()
    top_genres = df_clustering['listed_in'].str.split(', ').explode().str.strip().value_counts().head(20).index.tolist()
    for genre in top_genres:
        df_clustering[f'genre_{genre.lower().replace(" ", "_")}'] = df_clustering['listed_in'].str.contains(genre, case=False, na=False).astype(int)
    
    # Select features for clustering
    feature_cols = ['rating_numeric', 'duration_normalized'] + [f'genre_{genre.lower().replace(" ", "_")}' for genre in top_genres]
    X_cluster = df_clustering[feature_cols].fillna(0)
    
    # Scale features
    scaler = StandardScaler()
    X_cluster_scaled = scaler.fit_transform(X_cluster)
    
    # Apply K-Means with optimal k=4
    optimal_k = 4
    kmeans = KMeans(n_clusters=optimal_k, random_state=42, n_init=10)
    df_clustering['cluster'] = kmeans.fit_predict(X_cluster_scaled)
    
    return df_clustering, X_cluster_scaled

@st.cache_data
def train_classifier(df):
    # Prepare data for classification (predict 'type' based on features)
    df_class = df.copy()
    
    # Features
    df_class['duration_value'] = df_class['duration'].str.extract(r'(\d+)').astype(float)
    df_class['duration_normalized'] = df_class['duration_value'].copy()
    df_class.loc[df_class['type'] == 'TV Show', 'duration_normalized'] = \
        df_class.loc[df_class['type'] == 'TV Show', 'duration_normalized'].clip(upper=15)
    df_class.loc[df_class['type'] == 'Movie', 'duration_normalized'] = \
        df_class.loc[df_class['type'] == 'Movie', 'duration_normalized'].clip(upper=200)
    
    rating_map = {
        'G': 1, 'TV-Y': 1, 'TV-Y7': 2, 'TV-Y7-FV': 2, 'PG': 3, 'TV-PG': 3,
        'PG-13': 4, 'TV-14': 4, 'R': 5, 'TV-MA': 5, 'NC-17': 6, 'UR': 3, 'Unknown': 3
    }
    df_class['rating_numeric'] = df_class['rating'].map(rating_map).fillna(3)
    
    # Top genres
    top_genres = df_class['listed_in'].str.split(', ').explode().str.strip().value_counts().head(10).index.tolist()
    for genre in top_genres:
        df_class[f'genre_{genre.lower().replace(" ", "_")}'] = df_class['listed_in'].str.contains(genre, case=False, na=False).astype(int)
    
    feature_cols = ['rating_numeric', 'duration_normalized'] + [f'genre_{genre.lower().replace(" ", "_")}' for genre in top_genres]
    X = df_class[feature_cols].fillna(0)
    y = df_class['type']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train Random Forest
    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    
    # Predictions
    y_pred = clf.predict(X_test)
    
    # Feature importance
    feature_importance = pd.DataFrame({
        'feature': feature_cols,
        'importance': clf.feature_importances_
    }).sort_values('importance', ascending=False)
    
    return clf, X_test, y_test, y_pred, feature_importance

df = load_data()
df_clustering, X_cluster_scaled = prepare_clustering_data(df)
clf, X_test, y_test, y_pred, feature_importance = train_classifier(df)

# 3. Sidebar Filters
st.sidebar.header("Filter Data")

# Filter: Content Type
type_filter = st.sidebar.multiselect(
    "Content Type",
    options=df["type"].unique(),
    default=df["type"].unique()
)

# Filter: Release Year Range
min_year = int(df["release_year"].min())
max_year = int(df["release_year"].max())
year_filter = st.sidebar.slider(
    "Release Year",
    min_value=min_year,
    max_value=max_year,
    value=(2000, max_year)
)

# Filter: Country (Top 20 for cleaner UI, plus 'All')
top_countries = df[df['country'] != 'Unknown']['country'].value_counts().head(20).index.tolist()
country_filter = st.sidebar.multiselect(
    "Country (Top 20)",
    options=top_countries,
    default=[]
)

# Filter: Genre
genres = sorted(df['primary_genre'].unique().tolist())
genre_filter = st.sidebar.multiselect(
    "Primary Genre",
    options=genres,
    default=[]
)

# 4. Apply Filters to Dataset
filtered_df = df[
    (df["type"].isin(type_filter)) &
    (df["release_year"] >= year_filter[0]) &
    (df["release_year"] <= year_filter[1])
]

if country_filter:
    # Handle cases where multiple countries might be listed in the country column
    filtered_df = filtered_df[filtered_df["country"].apply(lambda x: any(c in x for c in country_filter))]

if genre_filter:
    filtered_df = filtered_df[filtered_df["primary_genre"].isin(genre_filter)]

# 5. Top-Level Metrics
st.markdown("### Quick Insights")
col1, col2, col3 = st.columns(3)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Total Movies", len(filtered_df[filtered_df['type'] == 'Movie']))
col3.metric("Total TV Shows", len(filtered_df[filtered_df['type'] == 'TV Show']))

st.divider()

# 6. Original Visualizations

col_chart1, col_chart2 = st.columns(2)

# Insight 1: Rating Analysis
with col_chart1:
    st.subheader("Rating Analysis")
    rating_counts = filtered_df['rating'].value_counts().reset_index()
    rating_counts.columns = ['rating', 'count']
    fig_rating = px.bar(
        rating_counts, 
        x='rating', 
        y='count', 
        color='rating',
        title="Content Distribution by Maturity Rating"
    )
    st.plotly_chart(fig_rating, width='stretch')

# Insight 2: Top Genres
with col_chart2:
    st.subheader("Top Genres Analysis")
    genre_counts = filtered_df['primary_genre'].value_counts().head(10).reset_index()
    genre_counts.columns = ['genre', 'count']
    fig_genre = px.pie(
        genre_counts, 
        names='genre', 
        values='count', 
        title="Top 10 Genres (Proportion)",
        hole=0.4
    )
    st.plotly_chart(fig_genre, width='stretch')

# Insight 3: Content Distribution by Country
st.subheader("Content Distribution by Top Producing Countries")
country_counts = filtered_df[filtered_df['country'] != 'Unknown']['country'].value_counts().head(15).reset_index()
country_counts.columns = ['country', 'count']
fig_country = px.bar(
    country_counts,
    x='count',
    y='country',
    orientation='h',
    title="Top 15 Content Producing Countries",
    color='count',
    color_continuous_scale=px.colors.sequential.Reds
)
fig_country.update_layout(yaxis={'categoryorder':'total ascending'})
st.plotly_chart(fig_country, width='stretch')

# Insight 4: Content trends over the years
st.subheader("Content Added Over Time (by Release Year)")
yearly_counts = filtered_df.groupby(['release_year', 'type']).size().reset_index(name='count')
fig_trend = px.line(
    yearly_counts, 
    x='release_year', 
    y='count', 
    color='type', 
    title="Movies vs TV Shows Released Over Time"
)
st.plotly_chart(fig_trend, width='stretch')

st.divider()

# 7. Additional Visualizations from Week-5 Analysis

# Content Growth Over Time
st.subheader("Netflix Content Growth Over Time")
content_growth = df.groupby('year_added').size().reset_index(name='count').sort_values('year_added')
content_growth = content_growth[content_growth['year_added'] > 0]  # Exclude invalid years

fig_growth = go.Figure()
fig_growth.add_trace(go.Scatter(
    x=content_growth['year_added'],
    y=content_growth['count'],
    mode='lines+markers',
    name='Titles Added',
    line=dict(color='#E50914', width=3),
    marker=dict(size=8)
))
fig_growth.update_layout(
    title='Netflix Content Growth Over Time',
    xaxis_title='Year Added',
    yaxis_title='Number of Titles',
    hovermode='x unified',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_growth, width='stretch')

# Growth by Content Type
st.subheader("Content Growth by Type (Movie vs TV Show)")
growth_by_type = df.groupby(['year_added', 'type']).size().reset_index(name='count')
growth_by_type = growth_by_type[growth_by_type['year_added'] > 0]

fig_type_growth = go.Figure()
for content_type in growth_by_type['type'].unique():
    data = growth_by_type[growth_by_type['type'] == content_type]
    fig_type_growth.add_trace(go.Scatter(
        x=data['year_added'],
        y=data['count'],
        mode='lines+markers',
        name=content_type.title(),
        line=dict(width=2),
        marker=dict(size=6)
    ))
fig_type_growth.update_layout(
    title='Netflix Content Growth by Type (Movie vs TV Show)',
    xaxis_title='Year Added',
    yaxis_title='Number of Titles',
    hovermode='x unified',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_type_growth, width='stretch')

# Cumulative Growth
st.subheader("Cumulative Content Growth")
content_growth['cumulative'] = content_growth['count'].cumsum()

fig_cumulative = go.Figure()
fig_cumulative.add_trace(go.Bar(
    x=content_growth['year_added'],
    y=content_growth['count'],
    name='Titles Added That Year',
    marker=dict(color='#E50914'),
    yaxis='y'
))
fig_cumulative.add_trace(go.Scatter(
    x=content_growth['year_added'],
    y=content_growth['cumulative'],
    name='Cumulative Total',
    line=dict(color='#221F1F', width=3),
    yaxis='y2',
    mode='lines+markers'
))
fig_cumulative.update_layout(
    title='Netflix Content Growth: Annual vs Cumulative',
    xaxis_title='Year Added',
    yaxis=dict(title='Titles Added That Year'),
    yaxis2=dict(title='Cumulative Total', overlaying='y', side='right'),
    hovermode='x unified',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_cumulative, width='stretch')

# Top 20 Countries Bar Chart
st.subheader("Top 20 Countries Contributing Netflix Content")
country_distribution = df[df['country'] != 'Unknown']['country'].value_counts().reset_index()
country_distribution.columns = ['country', 'count']
top_countries_viz = country_distribution.head(20).sort_values('count', ascending=True)

fig_top_countries = go.Figure(data=[go.Bar(
    y=top_countries_viz['country'],
    x=top_countries_viz['count'],
    orientation='h',
    marker=dict(color='#E50914')
)])
fig_top_countries.update_layout(
    title='Top 20 Countries Contributing Netflix Content',
    xaxis_title='Number of Titles',
    yaxis_title='Country',
    height=600
)
st.plotly_chart(fig_top_countries, width='stretch')

st.divider()

# 8. Clustering Analysis Visualizations

st.header("Content Clustering Analysis")
st.markdown("Netflix content has been clustered into 4 groups based on genre, duration, and rating using K-Means clustering.")

# PCA Visualization of Clusters
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_cluster_scaled)

cluster_colors = ['#E50914', '#221F1F', '#B81D13', '#564D4D']
cluster_names = {
    0: 'Short Movies\n(Documentaries/Family)',
    1: 'Standard Movies\n(Drama/International)',
    2: 'TV Shows\n(General Audience)',
    3: 'Kids TV Shows'
}

fig_pca = go.Figure()
for cluster_id in range(4):
    mask = df_clustering['cluster'] == cluster_id
    mask_indices = mask.values
    cluster_titles = df_clustering[mask]['title'].values[:100]  # Limit for performance
    fig_pca.add_trace(go.Scatter(
        x=X_pca[mask_indices, 0],
        y=X_pca[mask_indices, 1],
        mode='markers',
        name=f"Cluster {cluster_id}: {cluster_names[cluster_id].split(chr(10))[0]}",
        marker=dict(
            size=6,
            color=cluster_colors[cluster_id],
            opacity=0.7,
            line=dict(width=1, color='white')
        ),
        text=cluster_titles,
        hovertemplate='<b>%{text}</b><br>PC1: %{x:.2f}<br>PC2: %{y:.2f}<extra></extra>'
    ))

fig_pca.update_layout(
    title=f'Netflix Content Clusters (PCA Visualization)<br><sub>Explained Variance: PC1={pca.explained_variance_ratio_[0]:.1%}, PC2={pca.explained_variance_ratio_[1]:.1%}</sub>',
    xaxis_title=f'First Principal Component ({pca.explained_variance_ratio_[0]:.1%} variance)',
    yaxis_title=f'Second Principal Component ({pca.explained_variance_ratio_[1]:.1%} variance)',
    width=1000,
    height=600,
    template='plotly_white',
    hovermode='closest'
)
st.plotly_chart(fig_pca, width='stretch')

# Cluster Composition: Movie vs TV Show Distribution
cluster_type_dist = df_clustering.groupby(['cluster', 'type']).size().unstack(fill_value=0)

fig_cluster_type = go.Figure()
for content_type in ['Movie', 'TV Show']:
    if content_type in cluster_type_dist.columns:
        fig_cluster_type.add_trace(go.Bar(
            name=content_type.upper(),
            x=[f"Cluster {i}" for i in range(4)],
            y=cluster_type_dist[content_type],
            marker_color='#E50914' if content_type == 'Movie' else '#221F1F'
        ))

fig_cluster_type.update_layout(
    title='Cluster Composition: Movie vs TV Show Distribution',
    xaxis_title='Cluster',
    yaxis_title='Number of Titles',
    barmode='stack',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_cluster_type, width='stretch')

# Cluster Analysis: Rating Distribution
cluster_rating_dist = pd.crosstab(df_clustering['cluster'], df_clustering['rating'])

fig_cluster_rating = go.Figure()
for cluster_id in range(4):
    rating_counts = cluster_rating_dist.loc[cluster_id].sort_values(ascending=False).head(5)
    fig_cluster_rating.add_trace(go.Bar(
        name=f"Cluster {cluster_id}",
        x=rating_counts.index,
        y=rating_counts.values,
        marker_color=cluster_colors[cluster_id]
    ))

fig_cluster_rating.update_layout(
    title='Top 5 Ratings by Cluster',
    xaxis_title='Rating',
    yaxis_title='Number of Titles',
    barmode='group',
    template='plotly_white',
    height=500
)
st.plotly_chart(fig_cluster_rating, width='stretch')

# Cluster Analysis: Duration Distribution
fig_cluster_duration = go.Figure()
for cluster_id in range(4):
    cluster_durations = df_clustering[df_clustering['cluster'] == cluster_id]['duration_normalized']
    fig_cluster_duration.add_trace(go.Box(
        y=cluster_durations,
        name=f"Cluster {cluster_id}",
        marker_color=cluster_colors[cluster_id],
        boxmean='sd'
    ))

fig_cluster_duration.update_layout(
    title='Duration Distribution by Cluster',
    yaxis_title='Duration (minutes for movies, seasons for TV)',
    template='plotly_white',
    height=500,
    showlegend=True
)
st.plotly_chart(fig_cluster_duration, width='stretch')

# Cluster Summary
st.subheader("Cluster Interpretations")
cluster_interpretations = {
    0: {
        "name": "Short Documentary & Family Movies",
        "description": "Lower-duration films focused on documentaries, children's content, and comedies",
        "target_audience": "Families with children, documentary enthusiasts"
    },
    1: {
        "name": "Premium Drama & International Movies",
        "description": "Full-length dramatic films and international productions at standard cinema length",
        "target_audience": "Adult audiences, international content seekers"
    },
    2: {
        "name": "Mainstream TV Series",
        "description": "Standard TV shows for general audiences with 1-2 seasons typical",
        "target_audience": "General audience, TV series enthusiasts"
    },
    3: {
        "name": "Children's Programmed Shows",
        "description": "TV shows specifically designed for children with age-appropriate ratings",
        "target_audience": "Children, young families"
    }
}

for cluster_id in range(4):
    cluster_data = df_clustering[df_clustering['cluster'] == cluster_id]
    info = cluster_interpretations[cluster_id]
    with st.expander(f"Cluster {cluster_id}: {info['name']}"):
        st.write(f"**Size:** {len(cluster_data)} titles ({len(cluster_data)/len(df_clustering)*100:.1f}%)")
        st.write(f"**Description:** {info['description']}")
        st.write(f"**Target Audience:** {info['target_audience']}")
        movie_pct = (cluster_data['type'] == 'Movie').sum() / len(cluster_data) * 100
        tv_pct = (cluster_data['type'] == 'TV Show').sum() / len(cluster_data) * 100
        st.write(f"**Content Mix:** Movies {movie_pct:.0f}% | TV Shows {tv_pct:.0f}%")
        avg_duration = cluster_data['duration_normalized'].mean()
        duration_unit = "minutes" if movie_pct > tv_pct else "seasons"
        st.write(f"**Avg Duration:** {avg_duration:.1f} {duration_unit}")
        top_genres = cluster_data['listed_in'].str.split(', ').explode().str.strip().value_counts().head(3)
        st.write(f"**Top Genres:** {', '.join(top_genres.index.tolist())}")

st.divider()

# 9. Classification Analysis

st.header("Content Classification Analysis")
st.markdown("Predicting content type (Movie vs TV Show) using machine learning based on rating, duration, and genres.")

# Confusion Matrix
cm = confusion_matrix(y_test, y_pred)
cm_df = pd.DataFrame(cm, index=['Actual Movie', 'Actual TV Show'], columns=['Predicted Movie', 'Predicted TV Show'])

fig_cm = go.Figure(data=go.Heatmap(
    z=cm,
    x=['Predicted Movie', 'Predicted TV Show'],
    y=['Actual Movie', 'Actual TV Show'],
    colorscale='Blues',
    text=cm,
    texttemplate='%{text}',
    textfont={"size": 12},
    showscale=True
))
fig_cm.update_layout(
    title='Confusion Matrix: Content Type Classification',
    height=400
)
st.plotly_chart(fig_cm, width='stretch')

# Classification Report
st.subheader("Classification Report")
report = classification_report(y_test, y_pred, output_dict=True)
report_df = pd.DataFrame(report).transpose()
st.dataframe(report_df.style.format("{:.2f}"))

# Feature Importance
st.subheader("Feature Importance")
fig_importance = px.bar(
    feature_importance.head(10),
    x='importance',
    y='feature',
    orientation='h',
    title='Top 10 Features for Content Type Prediction'
)
st.plotly_chart(fig_importance, width='stretch')

# Raw Data View
if st.checkbox("Show Raw Data"):
    st.dataframe(filtered_df[['title', 'type', 'country', 'release_year', 'rating', 'listed_in']])