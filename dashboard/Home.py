from PIL import Image
import streamlit as st


#Define tab title and icon
st.set_page_config(
    page_title="Main Page",
    page_icon="🪐",
)

#Define logo
img = Image.open("dashboard/images/Nasa_space_apps_challenge.png").convert("RGBA")
st.logo(img, size="large")


# st.write("""
# NASA Space Apps Challenge
#Build a Space Biology Knowledge Engine
#""")
st.markdown("# NASA Space Apps Challenge")
st.markdown("## Build a Space Biology Knowledge Engine")
st.markdown("### Team: Overcooked")

#st.image("sunrise.jpg", caption="Sunrise by the mountains")
