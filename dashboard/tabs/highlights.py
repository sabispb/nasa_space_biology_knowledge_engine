import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

def render(df):
  

    df_recs = pd.read_csv('data/SB_publication_PMC_recommendations.csv', sep='|')
    df_recs = df_recs.rename(columns={"pmc": "PMID", "recommended_rank": "Rank","recommended_pmc": "PMID article","recommended_title":"Title", "recommended_link":"Link article"})


    st.markdown("# Highlights from Space Biology publications ")

    st.divider()

    st.header("Articles List")
    
    # --- Display filtered DataFrame ---
    event = st.dataframe(
        df,
        column_config={"link": st.column_config.LinkColumn(display_text="Open in PubMed")},
        width="stretch",
        column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'link'],
        hide_index=True,
        on_select="rerun",
        selection_mode="single-row",
    )

    # --- Display total number of filtered articles ---
    st.markdown(f"**Total articles displayed:** {len(df):,}")

    # --- Get selected article ---
    PMID = event.selection.rows
    filtered_df = df.iloc[PMID].reset_index()

    # --- Display content depending on selection ---

    if filtered_df.empty:
        # Only shown when nothing is selected
        st.subheader("Please, select an article.")
        st.markdown(
            "<span style='color:#D0D0D0; font-style:italic;'>No article selected.</span>",
            unsafe_allow_html=True
        )

    else:
        # --- Display simplified abstract ---
        st.header("Abstract simplified ✨")

        abstract_text = filtered_df['Abstract Simplified'].iloc[0]
        if pd.isna(abstract_text) or str(abstract_text).strip() == "":
            st.markdown(
                "<span style='color:#D0D0D0; font-style:italic;'>Not available.</span>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(abstract_text)

        st.divider()

        # --- Display main ideas ---
        st.header("Main Ideas from Selected Article ✨")

        main_ideas_text = filtered_df['Main Ideas'].iloc[0]
        if pd.isna(main_ideas_text) or str(main_ideas_text).strip() == "":
            st.markdown(
                "<span style='color:#D0D0D0; font-style:italic;'>Not available.</span>",
                unsafe_allow_html=True
            )
        else:
            st.markdown(main_ideas_text)
        st.divider()

        # --- Display recommendations ---
        st.header("Similar Articles")

        # --- Get PMID of selected article ---
        selected_pmid = filtered_df.loc[0, "PMID"]
        # --- Filter df_recs by PMID ---
        filtered_recs = df_recs[df_recs["PMID"] == selected_pmid]

        if not filtered_recs.empty:
            st.dataframe(
                filtered_recs,
                width="stretch",
                column_order=['Rank','Title','PMID article', 'Link article'],
                hide_index=True,
                column_config={
                    "Link article": st.column_config.LinkColumn(display_text="Open Article")
                }
            )
        else:
            st.markdown(
                "<span style='color:#D0D0D0; font-style:italic;'>No recommendations available for this article.</span>",
                unsafe_allow_html=True
            )
    
    st.divider()

