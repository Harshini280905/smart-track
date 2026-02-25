from flask import Flask, render_template, jsonify

app = Flask(__name__)

# In-memory database (can later replace with real DB)
tasks = [
    {"id": 1, "title": "Design Dashboard UI", "status": "In Progress"},
    {"id": 2, "title": "Dockerize Application", "status": "Pending"}
]

projects = [
    {"id": 1, "name": "SmartTrack DevOps", "owner": "Team Alpha"},
    {"id": 2, "name": "Automation Pipeline", "owner": "Backend Team"}
]

@app.route("/")
def dashboard():
    return render_template("dashboard.html")

@app.route("/tasks")
def tasks_page():
    return render_template("tasks.html")

@app.route("/projects")
def projects_page():
    return render_template("projects.html")

@app.route("/api/tasks")
def get_tasks():
    return jsonify(tasks)

@app.route("/api/projects")
def get_projects():
    return jsonify(projects)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)