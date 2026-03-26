import streamlit as st
from theme import apply_theme
apply_theme()

st.set_page_config(page_title="Insights", layout="wide")

st.title("🧠 Key Insights & Conclusions")

st.markdown("""
### 🔥 Major Insights from Netflix Dataset

- Netflix content has grown rapidly after 2015
- Movies dominate the platform (~70% of content)
- TV Shows are fewer but growing steadily
- United States contributes the highest content
- International Movies is the most popular genre
- Most content is rated TV-MA and TV-14
- Content addition peaked around 2018–2020

---

### 💡 Business Insights

- Netflix focuses more on **movies over series**
- Strong push towards **international content expansion**
- Increasing trend indicates **aggressive content strategy**
- Mature audience (TV-MA) dominates platform

---

### 🚀 Recommendations

- Invest more in **TV Shows (high retention)**
- Expand in **emerging markets (India, Asia)**
- Focus on **regional content production**
""")