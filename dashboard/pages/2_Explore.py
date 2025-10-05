import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

st.set_page_config(layout='wide')

df = pd.read_parquet('data/SB_publication_PMC_texts.parquet')
df.rename(columns={"pmc":"PMID","abstract":"Abstract","text":"Text", "title":"Title"}, inplace=True)
df['link'] = df['link'].astype("string")
df = df.sort_values(['PMID'], ascending=False)

img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")

st.markdown("# Space Biology publications ")

st.divider()
if False:
    # --- Custom CSS: apply your color scheme only to the sidebar ---
    st.markdown("""
    <style>
    /* Scope the styles only to the sidebar */
    section[data-testid="stSidebar"] label[data-testid="stWidgetLabel"] p {
        color: white !important;               /* label text in white */
        font-weight: 600 !important;
    }

    /* Main select bar (gray background, rounded corners, light border) */
    section[data-testid="stSidebar"] div[data-baseweb="select"] > div {
        background-color: #e6e6e6 !important;  /* gray background for bar */
        border-radius: 6px !important;
        border: 1px solid #c2c2c2 !important;
    }

    /* Text inside the bar and dropdown */
    section[data-testid="stSidebar"] div[data-baseweb="select"] span {
        color: black !important;               /* black text for readability */
    }

    /* Dropdown list items */
    section[data-testid="stSidebar"] ul[role="listbox"] li {
        color: black !important;               /* black text inside dropdown */
    }

    /* Selected tags inside the multiselect */
    section[data-testid="stSidebar"] span[data-baseweb="tag"] {
        background-color: white !important;    /* white background for tags */
        color: black !important;               /* black text inside tags */
        border: 1px solid #ccc !important;     /* light gray border */
        border-radius: 8px !important;
        font-weight: 500 !important;
    }
    </style>
    """, unsafe_allow_html=True)


    # --- Sidebar: filters ---
    st.sidebar.markdown("### Filters")

    # 1) Article Type filter (with 'All' option)
    article_types = sorted(df['Article Type'].dropna().unique())
    options_with_all = ["All"] + article_types

    selected_types = st.sidebar.multiselect(
        "Filter Publications by Article Type",
        options=options_with_all,
        default=["All"],
        key="article_type_filter"
    )

    # 2) Year range slider
    st.sidebar.markdown("###")

    year_min = int(df['Year'].min())
    year_max = int(df['Year'].max())

    year_range = st.sidebar.slider(
        "Publication Year",
        min_value=year_min,
        max_value=year_max,
        value=(year_min, year_max),
        step=1,
        key="year_filter"
    )

    # 3) Journal filter (with 'All' option)
    st.sidebar.markdown("###")
    journals = sorted(df['Journal'].dropna().unique())
    journal_options_with_all = ["All"] + journals

    selected_journals = st.sidebar.multiselect(
        "Filter by Journal",
        options=journal_options_with_all,
        default=["All"],
        key="journal_filter"
    )

    # --- Combine filters ---
    filtered_df = df.copy()

    # Filter by Article Type
    if "All" not in selected_types and selected_types:
        filtered_df = filtered_df[filtered_df['Article Type'].isin(selected_types)]

    # Filter by Year range
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])
    ]

    # Filter by Journal
    if "All" not in selected_journals and selected_journals:
        filtered_df = filtered_df[filtered_df['Journal'].isin(selected_journals)]


st.divider()

st.header("Articles List")
# --- Display filtered DataFrame ---
st.dataframe(data=df,
             hide_index=True,
             width="stretch",
             column_order=['Title', 'PMID', 'link'],
             column_config={"link": st.column_config.LinkColumn(display_text="Open in PubMed")},)

# --- Display total number of filtered articles ---
st.markdown(f"**Total articles displayed:** {len(filtered_df):,}")






