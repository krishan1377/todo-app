from flask import Flask, request, jsonify
import psycopg2
import os

app = Flask(__name__)

DB_HOST = os.environ.get("DB_HOST", "localhost")
DB_NAME = os.environ.get("DB_NAME", "todo_db")
DB_USER = os.environ.get("DB_USER", "postgres")
DB_PASS = os.environ.get("DB_PASS", "postgres")

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    )
    return conn

def init_db():
    """Create todos table if it doesn't exist"""
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id SERIAL PRIMARY KEY,
            task TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

# --- Call init_db() once at startup ---
init_db()

@app.route('/todos', methods=['GET'])
def get_todos():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT id, task, created_at FROM todos ORDER BY id DESC;')
    rows = cur.fetchall()
    cur.close()
    conn.close()
    todos = [{"id": r[0], "task": r[1], "created_at": r[2]} for r in rows]
    return jsonify(todos)

@app.route('/todos', methods=['POST'])
def add_todo():
    task = request.json.get('task')
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("INSERT INTO todos (task) VALUES (%s) RETURNING id;", (task,))
    new_id = cur.fetchone()[0]
    conn.commit()
    cur.close()
    conn.close()
    return jsonify({"id": new_id, "task": task})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)