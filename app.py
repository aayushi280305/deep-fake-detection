import streamlit as st
import yt_dlp
import tempfile
import cv2
import numpy as np
from tensorflow.keras.models import load_model

st.set_page_config(page_title="Deepfake Detector", layout="centered")
st.title("🛡️ Deepfake Video Detector")

# -------------------------------
# LOAD MODEL (only once)
# -------------------------------
@st.cache_resource
def load_my_model():
    return load_model("model.h5")   # 🔁 change if your model name is different

model = load_my_model()

# -------------------------------
# YOUTUBE DOWNLOAD FUNCTION
# -------------------------------
def download_youtube_video(url):

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    temp_path = temp_file.name

    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]',
        'outtmpl': temp_path,
        'noplaylist': True,
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return temp_path

    except Exception:
        st.error("⚠️ Failed to download video")
        return None


# -------------------------------
# FRAME EXTRACTION
# -------------------------------
def extract_frames(video_path, max_frames=20):

    cap = cv2.VideoCapture(video_path)
    frames = []

    while len(frames) < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        frame = cv2.resize(frame, (224, 224))  # ⚠️ must match model input
        frame = frame / 255.0
        frames.append(frame)

    cap.release()
    return np.array(frames)


# -------------------------------
# PREDICTION FUNCTION
# -------------------------------
def predict_video(video_path):

    frames = extract_frames(video_path)

    if len(frames) == 0:
        return "No frames extracted", 0

    predictions = model.predict(frames, verbose=0)

    avg_pred = np.mean(predictions)
    confidence = float(avg_pred)

    if avg_pred > 0.5:
        return "FAKE", confidence
    else:
        return "REAL", confidence


# -------------------------------
# INPUT METHOD
# -------------------------------
input_method = st.radio(
    "Choose Input Method:",
    ["Upload Video File", "YouTube Link"]
)

video_path = None


# -------------------------------
# UPLOAD OPTION
# -------------------------------
if input_method == "Upload Video File":

    uploaded_file = st.file_uploader("Upload a video", type=["mp4", "mov", "avi"])

    if uploaded_file:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_file.read())
        video_path = tfile.name


# -------------------------------
# YOUTUBE OPTION
# -------------------------------
elif input_method == "YouTube Link":

    yt_url = st.text_input("Paste YouTube URL")

    if st.button("Download Video") and yt_url:
        with st.spinner("Downloading video..."):
            video_path = download_youtube_video(yt_url)


# -------------------------------
# SHOW VIDEO
# -------------------------------
if video_path:

    st.success("✅ Video ready")
    st.video(video_path)

    if st.button("Run Deepfake Detection"):

        with st.spinner("Analyzing video..."):

            label, confidence = predict_video(video_path)

            if label == "REAL":
                st.success(f"🟢 REAL\nConfidence: {confidence:.2f}")

            elif label == "FAKE":
                st.error(f"🔴 FAKE\nConfidence: {confidence:.2f}")

            else:
                st.warning(label)
