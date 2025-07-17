import streamlit as st
import sqlite3

# App config
st.set_page_config(page_title="Health FRS", layout="centered")

# Hide default Streamlit UI
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

# Center Title
st.markdown(
    "<h1 style='text-align: center; font-family: Arial;'>Health <span style='color: red;'>FRS</span></h1>",
    unsafe_allow_html=True
)

# Replace this with your logo if needed
# st.image("logo.png", width=100)

# Login Form
with st.form("login_form", clear_on_submit=False):
    st.markdown("### ")
    username = st.text_input("User Id", placeholder="Enter User ID")
    password = st.text_input("Password", placeholder="Enter Password", type="password")
    login_btn = st.form_submit_button("LOGIN")

# Footer - App Version and Credits
st.markdown("""
    <div style='text-align: center; padding-top: 20px;'>
        <p style='font-size: 13px;'>App Version : 1.0.14</p>
        <p style='color: green; font-size: 14px;'>Designed & Developed By RNIT</p>
    </div>
""", unsafe_allow_html=True)

# DB Login Logic
if login_btn:
    conn = sqlite3.connect("frs.db")
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username=? AND password=?", (username, password))
    user = c.fetchone()
    conn.close()

    if user:
        st.success("Login successful!")
        st.switch_page("pages/1_Capture.py")
    else:
        st.error("Invalid credentials.")
