import sqlite3

# Connect to the database (or create it if not exists)
conn = sqlite3.connect("frs.db")
c = conn.cursor()

# Create users table
c.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)
''')

# Insert default admin user
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))

# Create face_captures table with geolocation and timestamp
c.execute('''
CREATE TABLE IF NOT EXISTS face_captures (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    image_path TEXT,
    face_encoding TEXT,
    latitude TEXT,
    longitude TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
''')

# Commit and close
conn.commit()
conn.close()

print("✅ Database initialized successfully.")
