# streamlit_show_graphs.py
import os
from glob import glob
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide", page_title="Saved Graphs Viewer")
st.title("Saved Graphs Viewer")

GRAPHS_DIR = "graphs"
os.makedirs(GRAPHS_DIR, exist_ok=True)

# find PNG/JPG files in the folder
image_paths = sorted(glob(os.path.join(GRAPHS_DIR, "*.png")) + glob(os.path.join(GRAPHS_DIR, "*.jpg")))

if not image_paths:
    st.warning(f"No images found in '{GRAPHS_DIR}'. Place your two graph images there and refresh.")
else:
    # If there are exactly two images, show them side-by-side; otherwise allow selection
    if len(image_paths) == 2:
        col1, col2 = st.columns(2)
        with col1:
            st.image(Image.open(image_paths[0]), use_column_width=True, caption=os.path.basename(image_paths[0]))
        with col2:
            st.image(Image.open(image_paths[1]), use_column_width=True, caption=os.path.basename(image_paths[1]))
    else:
        st.sidebar.header("Choose image to display")
        choice = st.sidebar.selectbox("Image", [os.path.basename(p) for p in image_paths])
        selected_path = os.path.join(GRAPHS_DIR, choice)
        st.image(Image.open(selected_path), use_column_width=True, caption=choice)

    st.markdown("---")
    st.write("Available files:")
    for p in image_paths:
        st.write(f"- {os.path.basename(p)}")