import sqlite3

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create the users table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        username TEXT NOT NULL UNIQUE,
        password TEXT NOT NULL
    )
''')

user_data = [
    ('user1', 'password1'),
    ('user2', 'password2'),
    ('user3', 'password3')
]

# Execute INSERT statements
cursor.executemany('INSERT INTO users (username, password) VALUES (?, ?)', user_data)

# Commit changes and close the connection
conn.commit()
conn.close()
