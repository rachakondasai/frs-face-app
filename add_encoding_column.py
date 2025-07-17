import sqlite3

conn = sqlite3.connect("frs.db")
c = conn.cursor()

try:
    c.execute("ALTER TABLE face_captures ADD COLUMN face_encoding TEXT")
    print("✅ Column 'face_encoding' added successfully.")
except sqlite3.OperationalError as e:
    print(f"⚠️ Column may already exist or failed: {e}")

conn.commit()
conn.close()
