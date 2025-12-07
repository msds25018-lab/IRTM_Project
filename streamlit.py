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
    st.markdown(
        '''
        The topic relevance over time plot starts with per-document topic assignments produced by your BERTopic model. Each article is passed through the saved model (using precomputed embeddings) and receives a topic id; those ids are added to the dataframe so every record has both a timestamp and a topic label. These document-level labels are the raw data used to measure how prominent each topic is in each time period.
        
        Next, documents are grouped into regular time bins (monthly in your code) by converting each article’s timestamp into a month period. For every combination of month and topic the code counts how many documents were assigned to that topic, producing a time-by-topic frequency tablewhere each cell is the number of documents for that topic in that month.
        
        To make values comparable across months with different article volumes, the frequency table is converted into proportions: each topic’s monthly count is divided by the total number of documents in that month. Those proportions are the topic relevance values — they represent the share of the month’s corpus that belongs to each topic, so they sum to 1 across topics for each month and allow direct comparison of topic prominence across time.
        
        Finally, the script selects the top topics by overall relevance (the topics with the largest summed proportions across all months) and plots their relevance series over the monthly time axis. Each plotted line shows how a topic’s share of coverage changes over time, making it easy to see growth, decline, seasonality, or persistent dominance in the news stream. 
        
        '''
    )

elif section == "Z-score":
    st.markdown("# Z-score")
    if heatmap_img:
        st.image(Image.open(heatmap_img), use_column_width=True, caption = "Z-score Heatmap")
    
    st.markdown(
        '''
        The z-score measures how unusual a topic’s current share of coverage is compared with its recent behavior. Starting from the normalized relevance matrix (topic proportion per time bin), compute a short-window rolling mean and rolling standard deviation for each topic, then standardize each month’s relevance by subtracting the rolling mean and dividing by the rolling standard deviation. Positive z-scores indicate above‑normal prominence; negative scores indicate below‑normal prominence.

        Before dividing, guard against instability by flooring the rolling standard deviation to a small positive value and replacing infinities or NaNs so the matrix stays numeric. The choice of rolling window controls sensitivity: a shorter window highlights short-term anomalies, a longer window smooths them out.

        To visualize, select the topics to show (for example, the top‑k by overall relevance), arrange the z-score data with topics as rows and time bins as columns, and plot a diverging heatmap centered at zero. Use readable time labels on the x-axis, human‑readable topic names on the y-axis, and a colorbar labeled “z-score” so viewers can quickly spot months with unusually high or low topic prominence.
        
        '''
    )

elif section == "Conclusion":
    st.markdown("<h1 style='text-align:center; font-size:64px; margin-top:40px;'>CONCLUSION</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:20px; margin-top:20px;'>Key takeaways and final remarks.</div>", unsafe_allow_html=True)


