import streamlit as st, cv2, os, sqlite3, face_recognition, numpy as np, base64
from datetime import datetime
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase

st.set_page_config(page_title="Capture Face", layout="centered")
st.title("📷 Capture Face")

os.makedirs("captured_faces", exist_ok=True)

def save_log(image):
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    fn = f"face_{ts}.jpg"
    path = f"captured_faces/{fn}"
    cv2.imwrite(path, image)
    encs = face_recognition.face_encodings(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    enc64 = base64.b64encode(encs[0]).decode() if encs else None
    db = sqlite3.connect("frs.db")
    c = db.cursor()
    c.execute("INSERT INTO face_captures(name,image_path,face_encoding) VALUES(?,?,?)",("admin",path,enc64))
    db.commit(); db.close()
    return path

class T(VideoTransformerBase):
    def __init__(self): self.img=None
    def transform(self, frame):
        img = frame.to_ndarray(format="bgr24"); self.img=img.copy()
        h,w=img.shape[:2]
        mask=np.zeros((h,w),dtype=np.uint8); cv2.circle(mask,(w//2,h//2),min(h,w)//3,255,-1)
        return cv2.bitwise_and(img,img,mask=mask)

ctx = webrtc_streamer(key="cap", video_transformer_factory=T)

if st.button("📸 Capture Again"):
    if ctx.video_transformer and ctx.video_transformer.img is not None:
        p = save_log(ctx.video_transformer.img)
        st.success(f"✅ Saved: {p}")
    else:
        st.error("No camera image")
