import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

def render():
    if False:
        df = pd.read_parquet('data/SB_publication_PMC_texts.parquet')
        df.rename(columns={"pmc":"PMID","abstract":"Abstract","text":"Text", "title":"Title"}, inplace=True)
        df['link'] = df['link'].astype("string")
        df = df.sort_values(['PMID'], ascending=False)

  
    img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
    st.logo(img, size="large")

    df_text = pd.read_parquet('data/SB_publication_PMC_texts.parquet')
    df_data = pd.read_csv('data/SB_publication_PMC_data.csv', sep='|')

    df_text['pmc'] = df_text['pmc'].astype("int64")

    df_merged = df_data.merge(
        df_text[['pmc', 'abstract', 'text']],
        on='pmc',
        how='left'
    )
    df_merged.rename(columns={"pmc":"PMID","article_type":"Article Type","journal":"Journal","publication_year":"Year", "title":"Title", "abstract":"Abstract","text":"Full text"}, inplace=True)
    df_merged['link'] = df_merged['link'].astype("string")
    df_merged = df_merged.sort_values(['Year','PMID'], ascending=False)


    st.markdown("# Highlights from Space Biology publications ")

    st.divider()

    st.header("Articles List")
    # --- Display filtered DataFrame ---
    st.dataframe(data=df_merged,
                hide_index=True,
                width="stretch",
                column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'link'],
                column_config={"link": st.column_config.LinkColumn(display_text="Open in PubMed")},)

    # --- Display total number of filtered articles ---
    st.markdown(f"**Total articles displayed:** {len(filtered_df):,}")