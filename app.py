from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__)

# Function to initialize the database
def initialize_database():
    conn = sqlite3.connect('train_database.db')
    cursor = conn.cursor()
    # Create trains table
    cursor.execute('''CREATE TABLE IF NOT EXISTS trains (
                        id INTEGER PRIMARY KEY,
                        name TEXT NOT NULL,
                        number TEXT NOT NULL,
                        source TEXT NOT NULL,
                        destination TEXT NOT NULL
                    )''')
    # Insert sample data into the trains table
    cursor.execute("INSERT INTO trains (name, number, source, destination) VALUES (?, ?, ?, ?)",
                   ('Express Train', '12345', 'City A', 'City B'))
    cursor.execute("INSERT INTO trains (name, number, source, destination) VALUES (?, ?, ?, ?)",
                   ('Local Train', '67890', 'City C', 'City D'))
    conn.commit()
    conn.close()

# Function to authenticate user
def authenticate_user(username, password):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    #cursor.execute("SELECT * FROM users WHERE username=? AND password= ?", (username, password))
    cursor.execute(f"SELECT * FROM users WHERE username='{username}' AND password= '{password}'")  
    user = cursor.fetchone()
    conn.close()
    return user

# Route for handling login
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = authenticate_user(username, password)
    if user:
        # Authentication successful, redirect to home page
        return redirect(url_for('home'))
    else:
        # Authentication failed, redirect back to login page
        return redirect(url_for('login_page'))

# Route for login page
@app.route('/')
def login_page():
    return render_template('login.html')

# Route for home page
@app.route('/home')
def home():
    return render_template('home.html', username="user")

# Route for handling search
@app.route('/search')
def search():
    query = request.args.get('query')
    # Perform search operations here based on the query
    # For example, fetch data from the database and return as JSON
    conn = sqlite3.connect('train_database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM trains WHERE name LIKE ? OR number LIKE ?", ('%' + query + '%', '%' + query + '%'))
    search_results = cursor.fetchall()
    conn.close()
    # Convert search results to JSON format
    results_json = [{'name': row[1], 'number': row[2], 'source': row[3], 'destination': row[4]} for row in search_results]
    return jsonify(results_json)

if __name__ == '__main__':
    initialize_database()  # Initialize the database
    app.run(debug=True)
