import streamlit as st
import sqlite3
from PIL import Image, ImageDraw
from io import BytesIO
import base64

# App config
st.set_page_config(page_title="Health FRS", layout="centered")

# Hide Streamlit default UI
st.markdown("""
    <style>
        #MainMenu, header, footer {visibility: hidden;}
        [data-testid="stSidebar"] {display: none;}
        .stApp {
            background-color: #ffeb99;
            padding-top: 30px;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.markdown(
    "<h1 style='text-align: center; font-family: Arial;'>Health <span style='color: red;'>FRS</span></h1>",
    unsafe_allow_html=True
)

# Department Mapping
departments = {
    "MLHP Bodabandla": "Haripriya",
    "MLHP Bangarupalyem": "Puneeth",
    "MLHP Moglimittoor": "Ravali",
    "MLHP Nalagampalli": "Manjusha"
}

# Login Form
with st.form("login_form", clear_on_submit=False):
    st.markdown("### ")
    username = st.text_input("User Id", placeholder="Enter User ID")
    password = st.text_input("Password", placeholder="Enter Password", type="password")
    department = st.selectbox("Select Department", list(departments.keys()))
    login_btn = st.form_submit_button("LOGIN")

# DB Login Logic
if login_btn:
    conn = sqlite3.connect("frs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        # Store session data
        st.session_state["username"] = username
        st.session_state["department"] = department
        st.session_state["mlhp_name"] = departments[department]

        st.success(f"Welcome {departments[department]} from {department}!")
        st.switch_page("pages/1_Capture.py")
    else:
        st.error("Invalid credentials.")

# Footer with circular image
def circular_image_base64(img_path, size=(60, 60)):
    img = Image.open(img_path).convert("RGB").resize(size)
    bigsize = (img.size[0] * 3, img.size[1] * 3)
    mask = Image.new('L', bigsize, 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0) + bigsize, fill=255)
    mask = mask.resize(img.size, Image.LANCZOS)
    img.putalpha(mask)
    output = BytesIO()
    img.save(output, format="PNG")
    return base64.b64encode(output.getvalue()).decode()

# Load circular image and show footer
try:
    img_base64 = circular_image_base64("rachakonda.png")
    footer_html = f"""
        <div style='text-align: center; margin-top: 30px;'>
            <img src="data:image/png;base64,{img_base64}" style="border-radius: 50%; width: 60px; height: 60px;"/>
            <div style="color: green; font-weight: bold; margin-top: 5px;">Designed & Developed by Rachakonda Sai</div>
            <div style="font-size: 13px;">App Version : 1.0.14</div>
        </div>
    """
except Exception as e:
    footer_html = """
        <div style='text-align: center; margin-top: 30px;'>
            <div style="color: green; font-weight: bold; margin-top: 5px;">Designed & Developed by Rachakonda Sai</div>
            <div style="font-size: 13px;">App Version : 1.0.14</div>
        </div>
    """

st.markdown(footer_html, unsafe_allow_html=True)
