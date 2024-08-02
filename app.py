from flask import Flask, render_template, request, jsonify
import psycopg2
import os

app = Flask(__name__)

# Database connection parameters
DB_HOST = os.environ.get('DB_HOST', 'postgres-service')
DB_NAME = os.environ.get('DB_NAME', 'sampledb')
DB_USER = os.environ.get('DB_USER', 'sampleuser')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'samplepassword')

def get_db_connection():
    conn = psycopg2.connect(host=DB_HOST, database=DB_NAME, user=DB_USER, password=DB_PASSWORD)
    return conn

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    # In a real application, you'd verify the password here
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
    user = cur.fetchone()
    cur.close()
    conn.close()

    if user:
        return jsonify({"success": True, "message": f"Welcome, {username}!"})
    else:
        return jsonify({"success": False, "message": "Invalid username"})

@app.route('/users')
def get_users():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM users')
    users = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(users)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=7000)