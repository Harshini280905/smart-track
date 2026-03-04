# SmartTrack — Team Project & Task Management Dashboard

> A full-stack web application for managing team projects and tasks with real-time user story tracking via GitHub Issues API.

---

## 📋 Features

- Create and manage multiple projects
- Add tasks with title, priority, assignee, and due date
- Update task status (Todo → In Progress → Done)
- REST API backend with JSON responses
- Fully containerized with Docker

---

## 📁 Project Structure

```
smarttrack-app/
├── app.py                 # Flask entry point
├── requirements.txt       # Python dependencies
├── Dockerfile             # Docker configuration
├── Jenkinsfile            # Jenkins pipeline
├── .github/workflows/     # GitHub Actions workflow
├── .gitignore
├── README.md
├── user-stories.md
├── templates/index.html   # Main frontend
├── static/style.css
├── models/database.py     # DB models
├── routes/
│   ├── projects.py
│   ├── tasks.py
│   └── stories.py         # GitHub API integration
└── tests/test_app.py
```
