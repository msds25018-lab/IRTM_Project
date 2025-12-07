# streamlit_single_page.py
import os
from glob import glob
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide", page_title="Saved Graphs Viewer")

GRAPHS_DIR = "graphs"
os.makedirs(GRAPHS_DIR, exist_ok=True)

# gather images
image_paths = sorted(glob(os.path.join(GRAPHS_DIR, "*.png")) + glob(os.path.join(GRAPHS_DIR, "*.jpg")))

st.sidebar.title("Navigation")
section = st.sidebar.radio("Go to", ("Welcome", "Introduction", "Topic Relevance", "Z-score", "Conclusion"))

def find_by_keywords(paths, keywords):
    for p in paths:
        name = os.path.basename(p).lower()
        for k in keywords:
            if k in name:
                return p
    return None

topic_img = find_by_keywords(image_paths, ("topic", "topics", "relevance"))
heatmap_img = find_by_keywords(image_paths, ("heatmap", "zscore", "z-score", "z_score"))

# simple fallbacks (minimal logic)
if not topic_img and image_paths:
    topic_img = image_paths[0]
if not heatmap_img and len(image_paths) > 1:
    heatmap_img = image_paths[1]
elif not heatmap_img and image_paths:
    heatmap_img = image_paths[0]

if section == "Welcome":
    st.markdown("<h1 style='text-align:center; font-size:72px; margin-top:40px;'>WELCOME</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; margin-top:20px;'>Welcome to the single-page viewer.</div>", unsafe_allow_html=True)

elif section == "Introduction":
    st.markdown("# Introduction")
    st.markdown(
        """
        **Purpose:** A compact single-page Streamlit app with left-side navigation.
        
        **Usage:** Use the sidebar to jump between sections. Place your PNG/JPG graphs in the `graphs/` folder.
        
        **Contents:** Welcome screen, an introduction, a topic relevance graph, a z-score heatmap, and a conclusion screen.
        """
    )

elif section == "Topic Relevance":
    st.markdown("# Topic Relevance")
    if topic_img:
        st.image(Image.open(topic_img), use_column_width=True, caption=os.path.basename(topic_img))

elif section == "Z-score":
    st.markdown("# Z-score")
    if heatmap_img:
        st.image(Image.open(heatmap_img), use_column_width=True, caption=os.path.basename(heatmap_img))

elif section == "Conclusion":
    st.markdown("<h1 style='text-align:center; font-size:64px; margin-top:40px;'>CONCLUSION</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; margin-top:20px;'>Key takeaways and final remarks.</div>", unsafe_allow_html=True)

# sidebar: list available files (minimal)
st.sidebar.markdown("### Available files")
for p in image_paths:
    st.sidebar.write(os.path.basename(p))
