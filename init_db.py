import sqlite3

conn = sqlite3.connect("frs.db")
c = conn.cursor()

# Create users table
c.execute('''CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password TEXT
)''')

# Add default admin user
c.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", ("admin", "admin123"))
conn.commit()
conn.close()
