from flask import Flask, jsonify, request
from flask_cors import CORS
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
CORS(app)

def get_connection():
    return psycopg2.connect(
        host="postgres",
        database="meubanco",
        user="admin",
        password="30xteleH@s88"
    )

@app.route("/")
def home():
    return jsonify({
        "message": "API do Meu Dia está online!",
        "status": "ok"
    })

@app.route("/create-table")
def create_table():
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            task_time TEXT,
            priority TEXT,
            done BOOLEAN DEFAULT FALSE,
            task_date DATE DEFAULT CURRENT_DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify({"message": "Tabela criada com sucesso!"})

@app.route("/tasks", methods=["GET"])
def get_tasks():
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        SELECT id, name, task_time, priority, done, task_date, created_at
        FROM tasks
        ORDER BY task_date DESC, task_time ASC, id DESC
    """)

    tasks = cursor.fetchall()

    cursor.close()
    connection.close()

    return jsonify(tasks)

@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()

    name = data.get("name")
    task_time = data.get("time", "Sem horário")
    priority = data.get("priority", "baixa")
    task_date = data.get("date")

    if not name:
        return jsonify({"error": "Nome da tarefa é obrigatório"}), 400

    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        INSERT INTO tasks (name, task_time, priority, task_date)
        VALUES (%s, %s, %s, COALESCE(%s::date, CURRENT_DATE))
        RETURNING id, name, task_time, priority, done, task_date, created_at
    """, (name, task_time, priority, task_date))

    task = cursor.fetchone()

    connection.commit()
    cursor.close()
    connection.close()

    return jsonify(task), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    connection = get_connection()
    cursor = connection.cursor(cursor_factory=RealDictCursor)

    cursor.execute("""
        UPDATE tasks
        SET done = NOT done
        WHERE id = %s
        RETURNING id, name, task_time, priority, done, task_date, created_at
    """, (task_id,))

    task = cursor.fetchone()
    connection.commit()

    cursor.close()
    connection.close()

    if not task:
        return jsonify({"error": "Tarefa não encontrada"}), 404

    return jsonify(task)

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    connection = get_connection()
    cursor = connection.cursor()

    cursor.execute("""
        DELETE FROM tasks
        WHERE id = %s
    """, (task_id,))

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({"message": "Tarefa excluída com sucesso"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)