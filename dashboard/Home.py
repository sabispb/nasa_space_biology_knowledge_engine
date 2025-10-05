from PIL import Image
import streamlit as st


#Define tab title and icon
st.set_page_config(layout='wide',
    page_title="Space Biology Publications",
    page_icon="🪐",
)

#Define logo
img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")


# st.write("""
# NASA Space Apps Challenge
#Build a Space Biology Knowledge Engine
#""")
st.markdown("# NASA Space Apps Challenge 🪐✨")
st.markdown("##")
st.markdown("""This project is the contribution of the team **Overcooked** to the [**Build a Space Biology Knowledge Engine**](https://www.spaceappschallenge.org/2025/challenges/build-a-space-biology-knowledge-engine/) challenge of the [**2025 NASA Space Apps Challenge**](https://www.spaceappschallenge.org/).

This project supports NASA's vision for safe and efficient human exploration of the Moon and Mars by developing a dynamic AI-powered dashboard that organizes, summarizes, and visualizes decades of space biology research. NASA's Biological and Physical Sciences Division has produced over 600 bioscience publications detailing experiments on how living systems respond to the space environment. However, the sheer volume and diversity of this information make it challenging to navigate.

This tool leverages data analytics and artificial intelligence to extract key insights, reveal research trends and gaps, and enable scientists, program managers, and mission planners to explore the impacts and outcomes of past space experiments through an interactive and accessible web interface.""")


col1, col2 = st.columns(2)

with col1:
    st.markdown("###")
    st.image(img)

with col2:
    st.markdown("###")
    st.markdown(""" ### Meet the Team Overcooked!

    | Name           | Email                 | GitHub | LinkedIn |
    |----------------|-----------------------|--------|----------|
    | Sabina Planas Bonell | sabinaplanas@gmail.com | [@sabispb](https://github.com/sabispb) | [sabina-planas-bonell](https://www.linkedin.com/in/sabina-planas-bonell/) |
    | Didac Fortuny Almiñana | dacfortuny@gmail.com | [@dacfortuny](https://github.com/dacfortuny) | [didacfortuny](https://www.linkedin.com/in/didacfortuny/) |""")




