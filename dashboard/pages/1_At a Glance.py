import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

from tabs import highlights, overview


st.set_page_config(layout='wide',
                    page_title="Space Biology Publications: At a Glance",
                    page_icon="🪐")

img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")

# ---------- Load data once (cached) ----------
@st.cache_data
def load_data():
    df_text_simplified = pd.read_parquet('data/SB_publication_PMC_texts_simplified.parquet')
    df_data = pd.read_csv('data/SB_publication_PMC_data.csv', sep='|')
    df_main_ideas = pd.read_parquet('data/SB_publication_PMC_texts_main_ideas.parquet')
    


    df_text_simplified['pmc'] = pd.to_numeric(df_text_simplified['pmc'], errors='coerce').astype('Int64')
    df_data['pmc'] = pd.to_numeric(df_data['pmc'], errors='coerce').astype('Int64')
    df_main_ideas['pmc'] = pd.to_numeric(df_data['pmc'], errors='coerce').astype('Int64')
    df_data['publication_year'] = pd.to_numeric(df_data['publication_year'], errors='coerce')

    df = df_data.merge(
        df_text_simplified[['pmc', 'abstract', 'text', 'simplified_abstract']],
        on='pmc',
        how='left'
    )

    df = df.merge(
        df_main_ideas[['pmc', 'main_ideas']],
        on='pmc',
        how='left'
    )

    df = df.rename(columns={
        "pmc": "PMID",
        "article_type": "Publication Type",
        "journal": "Journal",
        "publication_year": "Year",
        "title": "Title",
        "abstract": "Abstract",
        "text": "Full text",
        "simplified_abstract": "Abstract Simplified",
        "main_ideas": "Main Ideas",
    })
    df['link'] = df['link'].astype("string")
    df = df.sort_values(['Year', 'PMID'], ascending=False)
    return df

df_merged = load_data()

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

# ---------- Sidebar filters (shared) ----------
st.sidebar.markdown("### Filters")

# 1) Article Type
article_types = sorted(df_merged['Publication Type'].dropna().unique())
options_with_all = ["All"] + article_types
selected_types = st.sidebar.multiselect(
    "Filter by Publication Type",
    options=options_with_all,
    default=["All"],
    key="article_type_filter"
)

# 2) Year range
st.sidebar.markdown("###")
year_min = int(df_merged['Year'].min())
year_max = int(df_merged['Year'].max())
year_range = st.sidebar.slider(
    "Filter by Publication Year",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max),
    step=1,
    key="year_filter"
)

# 3) Journal
st.sidebar.markdown("###")
journals = sorted(df_merged['Journal'].dropna().unique())
journal_options_with_all = ["All"] + journals
selected_journals = st.sidebar.multiselect(
    "Filter by Journal",
    options=journal_options_with_all,
    default=["All"],
    key="journal_filter"
)

# ---------- Apply filters once ----------
filtered_df = df_merged.copy()
if "All" not in selected_types and selected_types:
    filtered_df = filtered_df[filtered_df['Publication Type'].isin(selected_types)]

filtered_df = filtered_df[
    (filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])
]

if "All" not in selected_journals and selected_journals:
    filtered_df = filtered_df[filtered_df['Journal'].isin(selected_journals)]


# --- Tabs ---
tab1, tab2 = st.tabs(["Overview", "Highlights"])
with tab1:
    overview.render(filtered_df)

with tab2:
    highlights.render(filtered_df)


