import os
from datetime import datetime

from flask import Flask, jsonify, request, render_template
from flasgger import Swagger, swag_from

import db
from auth import auth_bp
from middleware import token_required

PRIORITIES = ("low", "medium", "high")
PRIORITY_ORDER = {"high": 0, "medium": 1, "low": 2}

app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-only-secret")

# ---------------------------------------------------------------------------
# Swagger configuration
# ---------------------------------------------------------------------------

app.config["SWAGGER"] = {
    "title": "Task Manager API",
    "description": (
        "A RESTful API for managing personal tasks. "
        "Built with Flask and PostgreSQL. "
        "Authentication uses JWT Bearer tokens.\n\n"
        "**How to authenticate:**\n"
        "1. Register via `POST /auth/register`\n"
        "2. Login via `POST /auth/login` to receive your token\n"
        "3. Click **Authorize** and enter: `Bearer <your_token>`"
    ),
    "version": "1.0.0",
    "termsOfService": "",
    "uiversion": 3,
    "securityDefinitions": {
        "Bearer": {
            "type": "apiKey",
            "name": "Authorization",
            "in": "header",
            "description": "Enter your JWT token as: Bearer <token>",
        }
    },
}

swagger = Swagger(app)

# Register the auth blueprint (/auth/register and /auth/login)
app.register_blueprint(auth_bp)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def validate_date(date_string: str):
    if not date_string:
        return True, None

    try:
        date_obj = datetime.strptime(date_string, "%Y-%m-%d")
    except ValueError:
        return False, "Invalid date format. Use YYYY-MM-DD."

    today = datetime.now().date()
    if date_obj.date() < today:
        return False, f"Date cannot be in the past (today is {today})."

    return True, date_string


def sort_tasks(tasks):
    """Sort tasks: incomplete first, then by priority, then by due date."""
    return sorted(
        tasks,
        key=lambda t: (
            t["done"],
            PRIORITY_ORDER.get(t["priority"], 1),
            t["due_date"] or "9999-12-31",
        ),
    )


# ---------------------------------------------------------------------------
# Task routes — all protected by @token_required
# ---------------------------------------------------------------------------

@app.get("/tasks")
@token_required
def get_tasks(current_user):
    """
    Get all tasks for the authenticated user.
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    responses:
      200:
        description: A sorted list of all tasks belonging to the user.
        schema:
          type: array
          items:
            type: object
            properties:
              id:
                type: integer
                example: 1
              task:
                type: string
                example: "Finish Flask project"
              priority:
                type: string
                enum: [low, medium, high]
                example: "high"
              due_date:
                type: string
                example: "2026-05-01"
              done:
                type: boolean
                example: false
      401:
        description: Missing or invalid JWT token.
    """
    tasks = db.execute(
        """
        SELECT id, task, priority,
               TO_CHAR(due_date, 'YYYY-MM-DD') AS due_date,
               done
        FROM   tasks
        WHERE  user_id = %s
        """,
        (current_user["id"],),
        fetchall=True,
    )
    return jsonify(sort_tasks([dict(t) for t in tasks])), 200


@app.post("/tasks")
@token_required
def add_task(current_user):
    """
    Create a new task for the authenticated user.
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: body
        name: body
        required: true
        schema:
          type: object
          required:
            - task
          properties:
            task:
              type: string
              example: "Buy groceries"
            priority:
              type: string
              enum: [low, medium, high]
              default: medium
              example: "medium"
            due_date:
              type: string
              description: "Format: YYYY-MM-DD. Must not be in the past."
              example: "2026-06-15"
    responses:
      201:
        description: Task created successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task added."
      400:
        description: Validation error (missing task name, invalid priority, or past date).
      401:
        description: Missing or invalid JWT token.
    """
    data      = request.get_json(silent=True) or {}
    task_name = str(data.get("task", "")).strip()
    priority  = str(data.get("priority", "medium")).strip().lower()
    due_date  = str(data.get("due_date", "")).strip()

    if not task_name:
        return jsonify({"error": "Please enter a task name."}), 400

    if priority not in PRIORITIES:
        return jsonify({"error": "Priority must be low, medium, or high."}), 400

    is_valid, result = validate_date(due_date)
    if not is_valid:
        return jsonify({"error": result}), 400

    db.execute(
        """
        INSERT INTO tasks (user_id, task, priority, due_date)
        VALUES (%s, %s, %s, %s)
        """,
        (current_user["id"], task_name, priority, result),
    )

    return jsonify({"message": "Task added."}), 201


@app.post("/tasks/<int:task_id>/done")
@token_required
def mark_done(current_user, task_id: int):
    """
    Toggle the done/undone status of a task.
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: The ID of the task to toggle.
        example: 1
    responses:
      200:
        description: Task status updated successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task status updated."
      404:
        description: Task not found or does not belong to the user.
      401:
        description: Missing or invalid JWT token.
    """
    task = db.execute(
        "SELECT id, done FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, current_user["id"]),
        fetchone=True,
    )

    if not task:
        return jsonify({"error": "Task not found."}), 404

    db.execute(
        "UPDATE tasks SET done = %s WHERE id = %s",
        (not task["done"], task_id),
    )

    return jsonify({"message": "Task status updated."}), 200


@app.delete("/tasks/<int:task_id>")
@token_required
def delete_task(current_user, task_id: int):
    """
    Delete a task permanently.
    ---
    tags:
      - Tasks
    security:
      - Bearer: []
    parameters:
      - in: path
        name: task_id
        type: integer
        required: true
        description: The ID of the task to delete.
        example: 1
    responses:
      200:
        description: Task deleted successfully.
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Task deleted."
      404:
        description: Task not found or does not belong to the user.
      401:
        description: Missing or invalid JWT token.
    """
    task = db.execute(
        "SELECT id FROM tasks WHERE id = %s AND user_id = %s",
        (task_id, current_user["id"]),
    )

    if not task:
        return jsonify({"error": "Task not found."}), 404

    db.execute("DELETE FROM tasks WHERE id = %s", (task_id,))

    return jsonify({"message": "Task deleted."}), 200


# ---------------------------------------------------------------------------
# Frontend routes (no docs needed — these serve HTML pages)
# ---------------------------------------------------------------------------

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/login")
def login_page():
    return render_template("login.html")

@app.get("/register")
def register_page():
    return render_template("register.html")


# ---------------------------------------------------------------------------

if __name__ == "__main__":
    app.run(debug=True)