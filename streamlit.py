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
section = st.sidebar.radio("Go to", ("Welcome", "Introduction","Libraries", "Topic Relevance", "Z-score", "End"))

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
    st.markdown("<div style='text-align:center; font-size:16px; margin-top:8px;'></div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:16px; margin-top:8px;'>This dashboard provides a clear overview of the project and its key insights. Detailed explanations of the graphs, methods, and processing steps are available in the sections on the left. </div>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:center; font-size:16px; margin-top:8px;'>Thank you for taking the time to explore this work.</div>", unsafe_allow_html=True)

elif section == "Libraries":
    st.markdown("# Libraries")
    st.markdown("""
    ### Libraries and Tools

    #### Core data Manipulation
    - **pandas** — High-level data structures and utilities for loading, cleaning, transforming, and summarizing tabular data; used here to read JSON, manage timestamps, and group documents by time and topic.  
    - **numpy** — Fundamental numerical library for fast array operations and numeric computations used throughout preprocessing and matrix math.

    #### Visualization
    - **matplotlib.pyplot** — Low-level plotting API for creating figures, lines, labels, and saving images; used to draw the topic relevance line chart.  
    - **matplotlib.dates** — Date helpers for formatting and locating time ticks on plots (e.g., converting timestamps to readable year-month labels).  
    - **seaborn** — High-level statistical plotting built on Matplotlib; used to render the z-score heatmap with a clean default style and color mapping.

    #### Embedding and Topic Modeling
    - **SentenceTransformer** — Pretrained transformer models for producing dense sentence embeddings that capture semantic similarity; these embeddings are used as input to the topic model.  
    - **BERTopic** — Topic modeling library that clusters document embeddings and extracts interpretable topic keywords (c‑TF‑IDF); it assigns topic ids to documents and provides topic representations.

    #### Utilities
    - **os** — File and directory utilities for creating folders, joining paths, and checking file existence.  
    - **json** — Lightweight JSON encoder/decoder for reading and writing metadata such as the embedding model name or saved configuration.
    """, unsafe_allow_html=False)
    st.image(Image.open("app_assets/library.png"), use_column_width=True, caption="Libraries Used")




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
        The topic relevance over time is produced by the BERTopic model. Each article is passed through the saved model (using precomputed embeddings in the training code) and receives a topic id. These ids are added to the dataframe so every record has both a timestamp and a topic label. These labels are the raw data used to measure how prominent each topic is in each time period.
        
        Next, the documents are grouped into regular time bins (or time periods) by converting each article’s timestamp into a month period. For every combination of month and topic the code counts how many documents were assigned to that topic, producing a frequency table where each cell is the number of documents for that topic in that month.
        
        To make values comparable across months with different article volumes, the frequency table is converted into proportions. Each topic’s monthly count is divided by the total number of documents in that month. Those proportions are the topic relevance values. They represent the share of the month’s corpus that belongs to each topic, so they sum to 1 across topics for each month and allow direct comparison of topic prominence across time.
        
        Finally, the most relevant topics are selected and their relevance over months are plotted. Each plotted line shows how a topic’s share of relevance changes over time making it easy to analyze topics changes in the news stream. 
        
        '''
    )

elif section == "Z-score":
    st.markdown("# Z-score")
    if heatmap_img:
        st.image(Image.open(heatmap_img), use_column_width=True, caption = "Z-score Heatmap")
    
    st.markdown(
        '''
        The z-score measures how unusual a topic’s current relevance is compared with its recent past behavior. Starting from the normalized relevance matrix (topic proportion per time bin),  a short-window rolling mean and rolling standard deviation for each topic is calculated, then each month’s relevance is standardized by subtracting the rolling mean and dividing by the rolling standard deviation. Positive z-scores indicate above normal behaviour and negative scores indicate below normal beahviour.

        To visualize, topics are selected in a similar way for relevance and then arrange the z-score data with topics as rows and time bins as columns.
        
        '''
    )

elif section == "End":
    st.markdown("<h1 style='text-align:center; font-size:64px; margin-top:40px;'>Thank you</h1>", unsafe_allow_html=True)
    st.markdown("<div style='text-align:left; font-size:18px; margin-top:20px;'>For GitHub Repo : <a href='https://github.com/msds25018-lab/IRTM_Project.git' target='_blank'>Click here</a></div>",unsafe_allow_html=True)
    st.markdown("<div style='text-align:left; font-size:18px; margin-top:20px;'>For Presentation Slides : <a href='https://docs.google.com/presentation/d/1H5XrKFW9fphh4X7ZyiSIWpFNsyUE6hAgx7MrqISjZ8Q/edit?usp=sharing' target='_blank'>Click here</a></div>",unsafe_allow_html=True)
    st.markdown("<div style='text-align:left; font-size:18px; margin-top:20px;'>For Demo Video : <a href='' target='_blank'>Click here</a></div>",unsafe_allow_html=True)

