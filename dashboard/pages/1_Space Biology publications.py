import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px

from PIL import Image

st.set_page_config(layout='wide')

df = pd.read_csv('data/SB_publication_PMC_data.csv', sep='|')
df.rename(columns={"pmc":"PMID","article_type":"Article Type","journal":"Journal","publication_year":"Year"}, inplace=True)
df['Link'] = df['Link'].astype("string")

img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")

st.markdown("# Space Biology publications ")

st.divider()

col1, col2 = st.columns(2)

with col1:
    st.header("Journal")
    st.markdown("###")
    freq = df['Journal'].value_counts().to_dict()

    # Generate a word cloud image
    wordcloud = WordCloud(
        width=800,
        height=400,
        background_color='white',
        colormap='plasma'
    ).generate_from_frequencies(freq)

    # Create figure
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")

    # Display the generated image:
    st.pyplot(fig)

with col2:
    st.header("Title")

    fig = px.pie(
    df,
    names='Article Type',
    title='Type of articles'
)
    st.plotly_chart(fig, use_container_width=True)

st.divider()

# Count the number of articles per publication year
df_count = df['Year'].value_counts().sort_index().reset_index()
df_count.columns = ['Year', 'num_articles']

# Create a line chart with Plotly Express
fig = px.line(
    df_count,
    x='Year',
    y='num_articles',
    line_shape='spline',
    markers=True,
)

fig.update_xaxes(
    tickmode='linear',
    dtick=1,
    showgrid=True,
    gridcolor='lightgray',
    zeroline=False,
    color='black',         # make x-axis labels dark
    title_font=dict(color='black', size=16),
    tickfont=dict(color='black', size=14)
)

fig.update_yaxes(
    showgrid=True,
    gridcolor='lightgray',
    zeroline=False,
    color='black',         # make x-axis labels dark
    title_font=dict(color='black', size=16),
    tickfont=dict(color='black', size=14)
)

fig.update_traces(
    line=dict(color='#1f77b4', width=3),
    marker=dict(color='#1f77b4', size=6)
)

fig.update_layout(
    xaxis_title='Year of Publication',
    yaxis_title='Number of Articles',
    plot_bgcolor='white',         # chart background
    paper_bgcolor='white',        # outer background
    font=dict(color='black', size=14, family='Arial'),
    margin=dict(l=50, r=50, t=80, b=50)
    )

fig.layout.xaxis.title.font = dict(color='black', size=18, family='Arial Black')
fig.layout.yaxis.title.font = dict(color='black', size=18, family='Arial Black')

# Display the Plotly figure
st.plotly_chart(fig, use_container_width=True)

st.divider()
st.dataframe(data=df,
             hide_index=True,
             width="stretch",
             column_order=['Title', 'Journal', 'Article Type', 'Year', 'PMID', 'Link'],
             column_config={"Link": st.column_config.LinkColumn(display_text="Open in PubMed")},)




