def apply_netflix_theme():
    import streamlit as st

    st.markdown("""
    <style>
    /* 1. Overall App Background */
    .stApp {
        background-color: #000000 !important;
        color: white !important;
    }

    /* 2. Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #111111 !important;
        border-right: 1px solid #333;
    }

    /* 3. Force All Text to White (Headings, Labels, Paragraphs) */
    h1, h2, h3, h4, h5, h6, p, label, .stMarkdown, [data-testid="stMetricValue"] {
        color: white !important;
    }

    /* 4. Dropdown / Selectbox Fix (Dark Background & White Text) */
    div[data-baseweb="select"] > div {
        background-color: #1a1a1a !important;
        color: white !important;
        border: 1px solid #444 !important;
    }
    
    /* Dropdown list items */
    div[role="listbox"] {
        background-color: #1a1a1a !important;
    }
    div[role="option"] {
        color: white !important;
    }

    /* 5. MultiSelect Tags (Netflix Red) */
    div[data-baseweb="tag"] {
        background-color: #E50914 !important;
        color: white !important;
    }

    /* 6. Metric Cards Styling */
    div[data-testid="stMetric"] {
        background-color: #121212 !important;
        padding: 20px !important;
        border-radius: 10px !important;
        border: 1px solid #E50914 !important;
        box-shadow: 0px 4px 15px rgba(229, 9, 20, 0.2) !important;
    }

    /* 7. Radio Buttons Visibility */
    div[data-testid="stWidgetLabel"] p {
        color: white !important;
        font-weight: bold;
    }

    </style>
    """, unsafe_allow_html=True)