# streamlit_debug.py
import os
import sys
import traceback
from glob import glob
from PIL import Image
import streamlit as st

st.set_page_config(layout="wide", page_title="Streamlit Debug")

st.title("Streamlit Debug Smoke Test")
st.write("This page helps diagnose why your app shows a blank/black screen.")

# Basic environment info
st.subheader("Environment")
st.write("Working directory:", os.getcwd())
st.write("Python executable:", sys.executable)
st.write("Process id:", os.getpid())

# List top-level files (first 200 entries)
try:
    files = os.listdir(".")
    st.write("Files in working dir (first 200):", files[:200])
except Exception as e:
    st.error("Could not list working directory")
    st.text(traceback.format_exc())

# Check Streamlit config location and telemetry setting (if present)
st.subheader("Streamlit config and network checks")
home = os.path.expanduser("~")
config_path = os.path.join(home, ".streamlit", "config.toml")
st.write("User home:", home)
st.write("Streamlit config exists:", os.path.exists(config_path))
if os.path.exists(config_path):
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            st.code(f.read()[:2000])
    except Exception:
        st.write("Could not read config.toml")

# Attempt to load images from 'graphs' folder
st.subheader("Graphs folder check")
GRAPHS_DIR = "graphs"
if not os.path.exists(GRAPHS_DIR):
    st.warning(f"Folder '{GRAPHS_DIR}' not found in working dir.")
else:
    try:
        image_paths = sorted(glob(os.path.join(GRAPHS_DIR, "*.png")) + glob(os.path.join(GRAPHS_DIR, "*.jpg")))
        st.write(f"Found {len(image_paths)} image(s) in '{GRAPHS_DIR}'")
        if image_paths:
            # If exactly two images, show side-by-side
            if len(image_paths) == 2:
                col1, col2 = st.columns(2)
                with col1:
                    st.image(Image.open(image_paths[0]), use_column_width=True, caption=os.path.basename(image_paths[0]))
                with col2:
                    st.image(Image.open(image_paths[1]), use_column_width=True, caption=os.path.basename(image_paths[1]))
            else:
                # show thumbnails and allow selection
                for p in image_paths:
                    st.image(Image.open(p), width=400, caption=os.path.basename(p))
    except Exception as e:
        st.error("Error while loading images from graphs folder")
        st.text(traceback.format_exc())

# Try a minimal import of your app file (safe attempt)
st.subheader("Attempt to import your app module (no execution)")
APP_FILENAME = "streamlit.py"
if os.path.exists(APP_FILENAME):
    st.write(f"Found {APP_FILENAME}. Attempting to import it safely (no top-level execution).")
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("user_app_module", APP_FILENAME)
        module = importlib.util.module_from_spec(spec)
        # Do not execute module code; only show that spec was created
        st.success("Import spec created for your app file (did not execute it).")
    except Exception:
        st.error("Failed to create import spec for your app file")
        st.text(traceback.format_exc())
else:
    st.info(f"No {APP_FILENAME} found in working dir.")

st.markdown("---")
st.write("If this debug page renders correctly, the issue is inside your original app code (heavy blocking load or exception).")
st.write("If this page is also blank, the problem is likely browser/network/port or Streamlit process issues.")
