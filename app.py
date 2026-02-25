"""
SmartTrack — Team Project & Task Management Dashboard
Flask REST API Backend + HTML Frontend
PSG Assignment | 2025
"""

from flask import Flask, jsonify, request, render_template
import sqlite3
import os
import requests
from datetime import datetime

app = Flask(__name__)
DB_PATH = os.environ.get("DB_PATH", "smarttrack.db")
GITHUB_REPO = os.environ.get("GITHUB_REPO", "")  # e.g. "rajkumar/smarttrack-app"
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", "")


# ─── DB SETUP ─────────────────────────────────────────────────────────────────

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_db() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS projects (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                created_at TEXT DEFAULT (datetime('now'))
            );

            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                project_id INTEGER NOT NULL,
                title TEXT NOT NULL,
                description TEXT,
                assignee TEXT,
                priority TEXT DEFAULT 'Medium',
                status TEXT DEFAULT 'Todo',
                due_date TEXT,
                created_at TEXT DEFAULT (datetime('now')),
                FOREIGN KEY (project_id) REFERENCES projects(id)
            );
        """)


# ─── FRONTEND ─────────────────────────────────────────────────────────────────

@app.route("/")
def index():
    return render_template("index.html")


# ─── PROJECTS API ─────────────────────────────────────────────────────────────

@app.route("/api/projects", methods=["GET"])
def get_projects():
    with get_db() as conn:
        projects = conn.execute("SELECT * FROM projects ORDER BY created_at DESC").fetchall()
        result = []
        for p in projects:
            task_counts = conn.execute(
                "SELECT status, COUNT(*) as count FROM tasks WHERE project_id=? GROUP BY status",
                (p["id"],)
            ).fetchall()
            counts = {row["status"]: row["count"] for row in task_counts}
            result.append({
                "id": p["id"],
                "name": p["name"],
                "description": p["description"],
                "created_at": p["created_at"],
                "task_stats": counts
            })
    return jsonify(result)


@app.route("/api/projects", methods=["POST"])
def create_project():
    data = request.get_json()
    if not data or not data.get("name"):
        return jsonify({"error": "Project name is required"}), 400
    with get_db() as conn:
        cur = conn.execute(
            "INSERT INTO projects (name, description) VALUES (?, ?)",
            (data["name"], data.get("description", ""))
        )
        conn.commit()
        project_id = cur.lastrowid
    return jsonify({"id": project_id, "message": "Project created"}), 201


@app.route("/api/projects/<int:project_id>", methods=["DELETE"])
def delete_project(project_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE project_id=?", (project_id,))
        conn.execute("DELETE FROM projects WHERE id=?", (project_id,))
        conn.commit()
    return jsonify({"message": "Project deleted"}), 200


# ─── TASKS API ────────────────────────────────────────────────────────────────

@app.route("/api/projects/<int:project_id>/tasks", methods=["GET"])
def get_tasks(project_id):
    status_filter = request.args.get("status")
    assignee_filter = request.args.get("assignee")
    query = "SELECT * FROM tasks WHERE project_id=?"
    params = [project_id]
    if status_filter:
        query += " AND status=?"
        params.append(status_filter)
    if assignee_filter:
        query += " AND assignee=?"
        params.append(assignee_filter)
    query += " ORDER BY created_at DESC"
    with get_db() as conn:
        tasks = conn.execute(query, params).fetchall()
    return jsonify([dict(t) for t in tasks])


@app.route("/api/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    required = ["project_id", "title"]
    for field in required:
        if not data.get(field):
            return jsonify({"error": f"{field} is required"}), 400
    with get_db() as conn:
        cur = conn.execute(
            """INSERT INTO tasks (project_id, title, description, assignee, priority, due_date)
               VALUES (?, ?, ?, ?, ?, ?)""",
            (
                data["project_id"],
                data["title"],
                data.get("description", ""),
                data.get("assignee", "Unassigned"),
                data.get("priority", "Medium"),
                data.get("due_date", ""),
            )
        )
        conn.commit()
        task_id = cur.lastrowid
    return jsonify({"id": task_id, "message": "Task created"}), 201


@app.route("/api/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    allowed_statuses = ["Todo", "In Progress", "Done"]
    allowed_priorities = ["High", "Medium", "Low"]
    updates = {}
    if "status" in data and data["status"] in allowed_statuses:
        updates["status"] = data["status"]
    if "priority" in data and data["priority"] in allowed_priorities:
        updates["priority"] = data["priority"]
    if "assignee" in data:
        updates["assignee"] = data["assignee"]
    if not updates:
        return jsonify({"error": "No valid fields to update"}), 400
    set_clause = ", ".join(f"{k}=?" for k in updates)
    with get_db() as conn:
        conn.execute(
            f"UPDATE tasks SET {set_clause} WHERE id=?",
            list(updates.values()) + [task_id]
        )
        conn.commit()
    return jsonify({"message": "Task updated"})


@app.route("/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    with get_db() as conn:
        conn.execute("DELETE FROM tasks WHERE id=?", (task_id,))
        conn.commit()
    return jsonify({"message": "Task deleted"})


# ─── LIVE USER STORIES FROM GITHUB ────────────────────────────────────────────

@app.route("/api/stories", methods=["GET"])
def get_user_stories():
    """Fetch live user stories from GitHub Issues labeled 'user-story'"""
    if not GITHUB_REPO:
        # Return mock stories if GitHub repo not configured
        return jsonify({
            "source": "mock",
            "note": "Set GITHUB_REPO env variable to fetch live stories",
            "stories": [
                {"id": 1, "title": "US-01: User Registration", "state": "open", "labels": ["user-story", "High"], "url": "#"},
                {"id": 2, "title": "US-04: Create Project", "state": "open", "labels": ["user-story", "High"], "url": "#"},
                {"id": 3, "title": "US-08: Create Tasks", "state": "closed", "labels": ["user-story", "High"], "url": "#"},
                {"id": 4, "title": "US-13: Dashboard Stats", "state": "open", "labels": ["user-story", "Medium"], "url": "#"},
            ]
        })

    headers = {"Accept": "application/vnd.github.v3+json"}
    if GITHUB_TOKEN:
        headers["Authorization"] = f"token {GITHUB_TOKEN}"

    url = f"https://api.github.com/repos/{GITHUB_REPO}/issues?labels=user-story&state=all&per_page=50"
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        resp.raise_for_status()
        issues = resp.json()
        stories = [
            {
                "id": issue["number"],
                "title": issue["title"],
                "state": issue["state"],
                "body": issue.get("body", ""),
                "labels": [lbl["name"] for lbl in issue["labels"]],
                "url": issue["html_url"],
                "created_at": issue["created_at"],
            }
            for issue in issues
        ]
        return jsonify({"source": "github", "repo": GITHUB_REPO, "stories": stories})
    except requests.RequestException as e:
        return jsonify({"error": str(e)}), 503


# ─── HEALTH CHECK ─────────────────────────────────────────────────────────────

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "timestamp": datetime.utcnow().isoformat()})


# ─── MAIN ─────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    debug = os.environ.get("FLASK_DEBUG", "false").lower() == "true"
    print(f"SmartTrack running on http://0.0.0.0:{port}")
    app.run(host="0.0.0.0", port=port, debug=debug)
