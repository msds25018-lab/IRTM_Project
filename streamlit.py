import os
from glob import glob
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide", page_title="Saved Graphs Viewer")

GRAPHS_DIR = "graphs"
assets_dir = "app_assets"
os.makedirs(GRAPHS_DIR, exist_ok=True)

image_paths = sorted(glob(os.path.join(GRAPHS_DIR, "*.png")) + glob(os.path.join(GRAPHS_DIR, "*.jpg")))

st.sidebar.title("Please Select A Page Below")
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

if not topic_img and image_paths:
    topic_img = image_paths[0]
if not heatmap_img and len(image_paths) > 1:
    heatmap_img = image_paths[1]
elif not heatmap_img and image_paths:
    heatmap_img = image_paths[0]

if section == "Welcome":
    st.markdown("<h1 style='text-align:center; font-size:50px; margin-top:40px;'>Topic Relevance in News Streams Over Time</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:28px; margin-top:20px;'>IRTM Project Overview</div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:16px; margin-top:8px;'>BY: Umar Niazi - MSDS25018</div>", unsafe_allow_html=True)

elif section == "Introduction":
    st.markdown("# Introduction")
    st.markdown(
        """
        **Abstract:** This project aims to build a system that tracks the relevance of topics in news articles at times,
        using both category information and textual content (headlines and descriptions in this case).
        This project is directly aligned with the goals of Information Retrieval and Text Mining, as it
        demonstrates practical techniques for analysis of large text corpora.
        
        **Relevance With IRTM:** This project is relevant to Information Retrieval and Text Mining as it analyzes how topics evolve
        in news articles over time. By measuring and visualizing topic relevance, it reveals media
        coverage patterns, emerging trends, and provides valuable insights for journalists and
        researchers.
        
        
        Below is a summary diagram to summarise the work performed
        
        
        """
        
    )
    st.image(Image.open("app_assets/image.png"), use_column_width=True, caption="Summary Diagram")


elif section == "Topic Relevance":
    st.markdown("# Topic Relevance")
    if topic_img:
        st.image(Image.open(topic_img), use_column_width=True, caption = "Topic Relevance In News Over Time")

elif section == "Z-score":
    st.markdown("# Z-score")
    if heatmap_img:
        st.image(Image.open(heatmap_img), use_column_width=True, caption = "Z-score Heatmap")

elif section == "Conclusion":
    st.markdown("<h1 style='text-align:center; font-size:64px; margin-top:40px;'>CONCLUSION</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; margin-top:20px;'>Key takeaways and final remarks.</div>", unsafe_allow_html=True)


