from flask import Flask, request, jsonify
import psycopg2, os

app = Flask(__name__)

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_NAME = os.getenv("DB_NAME", "todo_db")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASS = os.getenv("DB_PASS", "password")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )
    return conn

@app.route("/todos", methods=["GET"])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM todos;")
    todos = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(todos)

@app.route("/todos", methods=["POST"])
def add_todo():
    data = request.get_json()
    task = data.get("task")
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id;", (task,))
    todo_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": todo_id, "task": task}), 201

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)