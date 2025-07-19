import streamlit as st
import cv2
import os
import sqlite3
import face_recognition
import numpy as np
import base64
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase
from streamlit_js_eval import streamlit_js_eval  # for geolocation

# Page setup
st.set_page_config(page_title="Capture Face", layout="centered")
st.title("📷 Capture Face")

# Ensure folder exists
os.makedirs("captured_faces", exist_ok=True)

# Get geolocation (optional)
geo = streamlit_js_eval(js_expressions="await new Promise((res, rej) => navigator.geolocation.getCurrentPosition(pos => res(pos.coords), err => res(null)))", key="get_geolocation")

if geo and "latitude" in geo and "longitude" in geo:
    latitude = geo["latitude"]
    longitude = geo["longitude"]
    st.success(f"📍 Location Captured: {latitude}, {longitude}")
else:
    latitude, longitude = None, None
    st.warning("⚠️ Location permission denied or unavailable.")

# Save face image and encoding to DB
def save_log(image, lat=None, lon=None):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"face_{ts}.jpg"
    path = f"captured_faces/{fn}"
    cv2.imwrite(path, image)
    encs = face_recognition.face_encodings(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enc64 = base64.b64encode(encs[0]).decode() if encs else None

    db = sqlite3.connect("frs.db")
    c = db.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS face_captures (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        image_path TEXT,
        face_encoding TEXT,
        latitude REAL,
        longitude REAL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute("INSERT INTO face_captures(name, image_path, face_encoding, latitude, longitude) VALUES (?, ?, ?, ?, ?)",
              ("admin", path, enc64, lat, lon))
    db.commit()
    db.close()
    return path

# Streamlit WebRTC transformer
class T(VideoTransformerBase):
    def __init__(self): self.img = None
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24")
        self.img = img.copy()
        h, w = img.shape[:2]
        mask = np.zeros((h, w), dtype=np.uint8)
        cv2.circle(mask, (w//2, h//2), min(h, w)//3, 255, -1)
        return cv2.bitwise_and(img, img, mask=mask)

ctx = webrtc_streamer(key="cap", video_transformer_factory=T)

# Capture Button
if st.button("📸 Capture Again"):
    if ctx.video_transformer and ctx.video_transformer.img is not None:
        p = save_log(ctx.video_transformer.img, latitude, longitude)
        st.success(f"✅ Saved: {p}")
    else:
        st.error("❌ No camera image detected!")
