import streamlit as st
import yt_dlp
import tempfile
import os

st.set_page_config(page_title="Deepfake Detector", layout="centered")

st.title("🛡️ Deepfake Video Detector")

# -------------------------------
# YouTube download function
# -------------------------------
def download_youtube_video(url):

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_path = temp_file.name

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': temp_path,
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return temp_path

    except Exception:
        st.error("⚠️ Failed to download video. Try another link or upload manually.")
        return None


# -------------------------------
# INPUT METHOD
# -------------------------------
input_method = st.radio(
    "Choose Input Method:",
    ["Upload Video File", "YouTube Link"]
)

video_path = None


# -------------------------------
# FILE UPLOAD
# -------------------------------
if input_method == "Upload Video File":

    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_file is not None:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        video_path = tfile.name


# -------------------------------
# YOUTUBE INPUT
# -------------------------------
elif input_method == "YouTube Link":

    yt_url = st.text_input(
        "Paste YouTube URL here",
        placeholder="https://youtube.com/watch?v=..."
    )

    if st.button("Download Video") and yt_url:
        with st.spinner("Downloading video..."):
            video_path = download_youtube_video(yt_url)


# -------------------------------
# SHOW VIDEO
# -------------------------------
if video_path:

    st.success("✅ Video ready for analysis")
    st.video(video_path)

    # -------------------------------
    # PLACEHOLDER FOR MODEL
    # -------------------------------
    if st.button("Run Deepfake Detection"):
        with st.spinner("Analyzing video..."):

            # 🔴 Replace this with your real model
            result = "REAL"  # or FAKE from your model

            if result == "REAL":
                st.success("🟢 This video appears to be REAL")
            else:
                st.error("🔴 Deepfake detected!")

    # Cleanup temp file after use (optional for deployment)
    # os.remove(video_path)
