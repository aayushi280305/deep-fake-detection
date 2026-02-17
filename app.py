import streamlit as st
import yt_dlp
import os
import cv2
import numpy as np
from mtcnn import MTCNN
from tensorflow.keras.models import load_model

# --- CONFIGURATION ---
TEMP_DIR = "data"
if not os.path.exists(TEMP_DIR):
    os.makedirs(TEMP_DIR)

TEMP_DOWNLOAD_PATH = os.path.join(TEMP_DIR, "video_input.mp4")

# --- FUNCTIONS ---
def download_youtube_video(url):
    ydl_opts = {
        'format': 'best', # Gets the best single file (video+audio) available
        'outtmpl': TEMP_DOWNLOAD_PATH,
        'noplaylist': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    return TEMP_DOWNLOAD_PATH

# --- UI INTERFACE ---
st.set_page_config(page_title="Deepfake Detection AI", page_icon="🛡️")
st.title("🛡️ Deepfake Video Detector")
st.info("Aayushi's BSc Data Science Practical Project")

# Input selection
option = st.sidebar.selectbox("Select Input Method", ("YouTube Link", "Local Upload"))

video_path = None

if option == "YouTube Link":
    url = st.text_input("Enter YouTube URL:")
    if url:
        if st.button("Fetch Video"):
            with st.spinner("Downloading..."):
                video_path = download_youtube_video(url)
                st.success("Video Ready!")

else:
    uploaded_file = st.file_uploader("Upload an MP4 file", type=["mp4"])
    if uploaded_file:
        with open(TEMP_DOWNLOAD_PATH, "wb") as f:
            f.write(uploaded_file.getbuffer())
        video_path = TEMP_DOWNLOAD_PATH

# --- ANALYSIS ENGINE ---
if video_path:
    st.video(video_path)
    
    if st.button("🚀 Start Deep Learning Analysis"):
        st.warning("Analyzing facial consistency and artifact patterns...")
        
        # Placeholder for Model Prediction
        # In your real project, you would use:
        # model = load_model('models/deepfake_model.h5')
        # result = model.predict(processed_frames)
        
        # For Demonstration Purposes:
        st.subheader("Result:")
        st.error("🚨 FAKE DETECTED (Confidence: 89.4%)")
        st.progress(89)
        st.write("Reasoning: Unnatural facial flickering detected in frame transitions.")
