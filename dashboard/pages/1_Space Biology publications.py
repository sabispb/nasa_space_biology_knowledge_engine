import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go

from PIL import Image

from tabs import general_info
from tabs import highlights

st.set_page_config(layout='wide')


tab1, tab2 = st.tabs(["General Information", "Highlights"])
with tab1:
    general_info.render()

with tab2:
    highlights.render()



