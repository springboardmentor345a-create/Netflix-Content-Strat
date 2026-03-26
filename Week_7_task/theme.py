def apply_theme():
    import streamlit as st
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

    /* Dropdown fix */
    div[data-baseweb="select"] > div {
        background-color: #1f1f1f !important;
        color: white !important;
    }

    div[data-baseweb="popover"] > div,
    ul[role="listbox"] {
        background-color: #1f1f1f !important;
    }

    li[role="option"] {
        background-color: #1f1f1f !important;
        color: white !important;
    }

    li[role="option"]:hover,
    li[aria-selected="true"] {
        background-color: #E50914 !important;
    }

    /* Text */
    h1, h2, h3, h4, h5, h6, p, span, div {
        color: white !important;
    }

    /* Table */
    [data-testid="stDataFrame"] table {
        background-color: #1f1f1f !important;
        color: white !important;
    }

    [data-testid="stDataFrame"] th {
        background-color: #000000 !important;
        color: #E50914 !important;
    }

    </style>
    """, unsafe_allow_html=True)