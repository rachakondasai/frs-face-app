import streamlit as st, sqlite3, os
st.set_page_config(page_title="Viewed Captures", layout="wide")
st.title("🗂️ Captured Faces History")
db=sqlite3.connect("frs.db"); c=db.cursor()
c.execute("SELECT id,name,image_path,timestamp FROM face_captures ORDER BY timestamp DESC")
for _id,name,path,ts in c.fetchall():
    cols = st.columns([1,3])
    cols[0].image(path, width=150) if os.path.exists(path) else cols[0].write("Missing")
    cols[1].markdown(f"**ID:** {_id}  \n**Name:** {name}  \n**When:** {ts}")
db.close()
