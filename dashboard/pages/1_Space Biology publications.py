import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

st.set_page_config(layout='wide')

df = pd.read_csv('data/SB_publication_PMC_data.csv', sep='|')
df.rename(columns={"pmc":"PMID","article_type":"Article Type","journal":"Journal","publication_year":"Year"}, inplace=True)
df['Link'] = df['Link'].astype("string")
df = df.sort_values(['Year','PMID'], ascending=False)

img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")

st.markdown("# Space Biology publications ")

st.divider()

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

# --- Combine both filters ---
filtered_df = df.copy()

# Apply Article Type filter (if not "All")
if "All" not in selected_types and selected_types:
    filtered_df = filtered_df[filtered_df['Article Type'].isin(selected_types)]

# Apply Year range filter (inclusive)
filtered_df = filtered_df[
    (filtered_df['Year'] >= year_range[0]) & (filtered_df['Year'] <= year_range[1])
]


col1, col2 = st.columns(2)

with col1:
    st.header("Distribution of Articles by Type")

    fig = px.pie(
    filtered_df,
    names='Article Type',
    
)
    st.plotly_chart(fig, use_container_width=True)

with col2:
    st.header("Number of Articles per Journal")

    # Radio in horizontal layout (options side by side)
    order = st.radio(
        "Order:",
        options=["Most articles", "Fewest articles"],
        horizontal=True,
        key="journal_order_radio"
        )

    # --- Data preparation ---
    freq = filtered_df['Journal'].value_counts().reset_index()
    freq.columns = ['Journal', 'Number of Articles']

    ascending = True if order == "Fewest articles" else False
    freq_sorted = freq.sort_values(by="Number of Articles", ascending=ascending)


    # --- Display table ---
    st.dataframe(freq_sorted, use_container_width=True, hide_index=True)
    
    # --- Display total count of journals ---
    st.markdown(f"**Total journals displayed:** {len(freq_sorted):,}")

    
st.divider()

st.header("Evolution of Articles per Year")
# --- Count number of articles per publication year ---
df_count = filtered_df['Year'].value_counts().sort_index().reset_index()
df_count.columns = ['Year', 'num_articles']

# --- Ensure all years are represented, even with 0 articles ---
year_min, year_max = filtered_df['Year'].min(), filtered_df['Year'].max()
full_year_range = pd.Series(range(year_min, year_max + 1), name='Year')

# Reindex to include missing years (fill with 0)
df_count = full_year_range.to_frame().merge(df_count, on='Year', how='left').fillna(0)

# --- Plot with Plotly Express ---
fig = px.line(
    df_count,
    x='Year',
    y='num_articles',
    line_shape='spline',
    markers=True,
)

# --- Axes styling ---
fig.update_xaxes(
    tickmode='linear',
    dtick=1,
    showgrid=True,
    gridcolor='lightgray',
    zeroline=False,
    color='black',
    tickfont=dict(color='black', size=14),
    title=None
)

fig.update_yaxes(
    showgrid=True,
    gridcolor='lightgray',
    zeroline=False,
    color='black',
    tickfont=dict(color='black', size=14),
    title=None
)

# --- Line and marker styling ---
fig.update_traces(
    line=dict(color='#1f77b4', width=3),
    marker=dict(color='#1f77b4', size=6)
)

# --- Layout ---
fig.update_layout(
    plot_bgcolor='white',
    paper_bgcolor='white',
    font=dict(color='black', size=14, family='Arial'),
    margin=dict(l=50, r=50, t=80, b=50)
)



# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True)

st.divider()


# --- Display filtered DataFrame ---
st.dataframe(data=filtered_df,
             hide_index=True,
             width="stretch",
             column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'Link'],
             column_config={"Link": st.column_config.LinkColumn(display_text="Open in PubMed")},)

# --- Display total number of filtered articles ---
st.markdown(f"**Total articles displayed:** {len(filtered_df):,}")




