import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

def render(df):
    
    st.markdown("# Space Biology publications ")

    st.divider()


    col1, col2 = st.columns(2)

    with col1:
        st.header("Distribution of Articles by Type")
        st.markdown("##")
        fig = px.pie(
        df,
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
        freq = df['Journal'].value_counts().reset_index()
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
    df_count = df['Year'].value_counts().sort_index().reset_index()
    df_count.columns = ['Year', 'num_articles']

    # --- Ensure all years are represented, even with 0 articles ---
    year_min, year_max = df['Year'].min(), df['Year'].max()
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
        title=None,
        range=[0, df_count["num_articles"].max() * 1.1]
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

    st.header("Articles List")
    # --- Display filtered DataFrame ---
    st.dataframe(data=df,
                hide_index=True,
                width="stretch",
                column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'link'],
                column_config={"link": st.column_config.LinkColumn(display_text="Open in PubMed")},)

    # --- Display total number of filtered articles ---
    st.markdown(f"**Total articles displayed:** {len(df):,}")