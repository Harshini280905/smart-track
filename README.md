# SmartTrack — Team Project & Task Management Dashboard

![Python](https://img.shields.io/badge/Python-3.11-blue) ![Flask](https://img.shields.io/badge/Flask-3.0-green) ![Docker](https://img.shields.io/badge/Docker-Ready-blue) ![CI/CD](https://img.shields.io/badge/CI%2FCD-Jenkins%20%7C%20GitHub%20Actions-orange)

> A full-stack web application for managing team projects and tasks with real-time user story tracking via GitHub Issues API.

---

## 📋 Features

- Create and manage multiple projects
- Add tasks with title, priority, assignee, and due date
- Update task status (Todo → In Progress → Done)
- Dashboard with live progress charts
- Real-time user stories fetched from GitHub Issues
- REST API backend with JSON responses
- Fully containerized with Docker

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.11, Flask 3.0 |
| Database | SQLite (via SQLAlchemy) |
| Frontend | HTML5, Bootstrap 5, Chart.js |
| Containerization | Docker |
| CI/CD | Jenkins / GitHub Actions |
| Registry | DockerHub |
| Cloud | AWS EC2 (t2.micro) |

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

---

## 🚀 Running Locally

```bash
# Clone the repository
git clone https://github.com/<your-username>/smarttrack-app.git
cd smarttrack-app

# Create virtual environment
python3 -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the app
python app.py

# Visit: http://localhost:5000
```

---

## 🐳 Running with Docker

```bash
# Pull from DockerHub
docker pull <dockerhub-username>/smarttrack-app:latest

# Run the container
docker run -p 5000:5000 <dockerhub-username>/smarttrack-app:latest

# Visit: http://localhost:5000
```

Or build locally:
```bash
docker build -t smarttrack-app .
docker run -p 5000:5000 smarttrack-app
```

---

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Dashboard homepage |
| GET | `/api/projects` | List all projects |
| POST | `/api/projects` | Create a project |
| DELETE | `/api/projects/<id>` | Delete a project |
| GET | `/api/projects/<id>/tasks` | List tasks for a project |
| POST | `/api/tasks` | Create a task |
| PUT | `/api/tasks/<id>` | Update task status |
| DELETE | `/api/tasks/<id>` | Delete a task |
| GET | `/api/stories` | Fetch live user stories from GitHub Issues |

---

## 🧪 Running Tests

```bash
python -m pytest tests/ -v
```

---

## 👥 Team Members

| Name | Role | GitHub |
|------|------|--------|
| Rajkumar | Lead Developer, DevOps, Backend | @rajkumar |
| Member 2 | Frontend, Testing | @member2 |
| Member 3 | Documentation, Cloud Setup | @member3 |

---

## 🔗 DockerHub

```
https://hub.docker.com/r/<dockerhub-username>/smarttrack-app
```

---

## ☁️ AWS Deployment (Nice to Have)

The app is deployed on an AWS EC2 `t2.micro` instance. Stage 4 of the pipeline SSHes into the instance, pulls the latest Docker image, and restarts the container.

Access the live app at: `http://<ec2-public-ip>:5000`

---

*PSG Assignment | SmartTrack | 2025*
