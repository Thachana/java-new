from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

db = mysql.connector.connect(
    host="db",
    user="root",
    password="root",
    database="crud_db"
)
cursor = db.cursor()

@app.route('/')
def home():
    return "Welcome to CRUD App!"

@app.route('/add', methods=['POST'])
def add_user():
    data = request.get_json()
    cursor.execute("INSERT INTO users (name) VALUES (%s)", (data['name'],))
    db.commit()
    return jsonify({"message": "User added"}), 201

@app.route('/users')
def list_users():
    cursor.execute("SELECT * FROM users")
    result = cursor.fetchall()
    return jsonify(result)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
