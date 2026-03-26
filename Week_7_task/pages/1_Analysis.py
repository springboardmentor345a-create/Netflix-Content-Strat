import streamlit as st
import pandas as pd
import plotly.express as px

from theme import apply_theme
apply_theme()

st.set_page_config(page_title="Analysis", layout="wide")

df = pd.read_csv("netflix_final.csv")

st.title("📊 Detailed Analysis")

# Rating Distribution
st.subheader("⭐ Rating Distribution")
rating_dist = df['rating'].value_counts()

fig = px.bar(x=rating_dist.index, y=rating_dist.values,
             color_discrete_sequence=["#E50914"])
fig.update_layout(
    plot_bgcolor="#1f1f1f",
    paper_bgcolor="#141414",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)

# Trend
st.subheader("📈 Content Trend Over Years")
trend = df.groupby('release_year').size()

fig = px.line(x=trend.index, y=trend.values)
fig.update_traces(line_color="#E50914")
fig.update_layout(
    plot_bgcolor="#1f1f1f",
    paper_bgcolor="#141414",
    font_color="white"
)
st.plotly_chart(fig, use_container_width=True)