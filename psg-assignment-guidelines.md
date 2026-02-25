# PSG Assignment Guidelines — SmartTrack Application
### Team Project (3 Members) | DevOps & Cloud Deployment Assessment

---

## 📌 Application Chosen: SmartTrack — Team Project & Task Management Dashboard

**Description:**
SmartTrack is a full-stack web application that allows teams to create projects, assign tasks, track priorities, and visualize progress in real time. It uses a Python Flask REST API backend with an HTML/JS frontend, connected to a SQLite database. User stories are fetched dynamically from the GitHub Issues API of the project repository, making them always up to date.

**Why this application:**
- Realistic enterprise use case
- Demonstrates REST API design, Dockerization, and CI/CD pipeline
- Real-time user story fetching adds unique technical depth
- Medium-scale: enough features to distribute across 3 team members, yet focused enough to complete solo

---

## 1. Application Scope — Broken Down to User Stories

User stories are fetched live from: `https://api.github.com/repos/<your-username>/smarttrack-app/issues?labels=user-story`

### Epic 1: User & Authentication Module
| Story ID | User Story | Priority |
|----------|-----------|----------|
| US-01 | As a user, I want to register with my name, email, and password so that I can access the application | High |
| US-02 | As a user, I want to log in and receive a session token so that my data is secure | High |
| US-03 | As an admin, I want to manage team members so that I can add or remove collaborators | Medium |

### Epic 2: Project Management Module
| Story ID | User Story | Priority |
|----------|-----------|----------|
| US-04 | As a user, I want to create a new project with a name and description so that I can organize work | High |
| US-05 | As a user, I want to view all projects I am a member of so that I can track progress | High |
| US-06 | As a user, I want to delete a project I own so that completed work is archived | Medium |
| US-07 | As a user, I want to assign team members to a project so that responsibilities are clear | Medium |

### Epic 3: Task Management Module
| Story ID | User Story | Priority |
|----------|-----------|----------|
| US-08 | As a user, I want to create tasks under a project with title, description, assignee, and priority so that work is tracked | High |
| US-09 | As a user, I want to update the status of a task (Todo / In Progress / Done) so that my team sees real-time progress | High |
| US-10 | As a user, I want to filter tasks by status or assignee so that I can manage my workload | Medium |
| US-11 | As a user, I want to set a due date for tasks so that deadlines are visible | Medium |
| US-12 | As a user, I want to delete tasks that are no longer relevant | Low |

### Epic 4: Dashboard & Reporting Module
| Story ID | User Story | Priority |
|----------|-----------|----------|
| US-13 | As a user, I want to see a dashboard with task completion stats per project so that I understand team velocity | High |
| US-14 | As a user, I want to see tasks grouped by priority (High / Medium / Low) in a visual chart | Medium |
| US-15 | As a user, I want live user stories fetched from GitHub Issues on the app's about page so that stakeholders see real requirements | Medium |

### Epic 5: DevOps & Deployment
| Story ID | User Story | Priority |
|----------|-----------|----------|
| US-16 | As a developer, I want the application to be containerized using Docker so it runs consistently across environments | High |
| US-17 | As a developer, I want a Jenkins/GitHub Actions pipeline to automate build, test, and deploy on every push | High |
| US-18 | As a developer, I want the Docker image pushed to DockerHub automatically on successful pipeline runs | High |
| US-19 | As a DevOps engineer, I want to deploy the container to an AWS EC2 instance via pipeline stage 4 | Nice to Have |

---

## 2. GitHub Repository Setup

- **Repository Name:** `smarttrack-app`
- **Visibility:** Public
- **Branch Strategy:**
  - `main` — production-ready code only
  - `develop` — integration branch
  - `feature/<story-id>-<short-name>` — individual feature branches
- **Code promotion to `main` must use Pull Requests only (no direct push)**
- Collaborators to be added: (add all 3 team member GitHub usernames)
- Branch protection rules to be set on `main`:
  - Require PR reviews before merging
  - Require status checks (CI pipeline) to pass before merging

---

## 3. Repository Structure

```
smarttrack-app/
├── app.py                    # Flask application entry point
├── requirements.txt          # Python dependencies
├── Dockerfile                # Docker build configuration
├── Jenkinsfile               # Jenkins CI/CD pipeline
├── .github/
│   └── workflows/
│       └── ci-cd.yml         # GitHub Actions CI/CD (alternative to Jenkins)
├── .gitignore                # Git ignore rules
├── README.md                 # Project documentation
├── user-stories.md           # Full user story documentation
├── templates/
│   └── index.html            # Frontend HTML template
├── static/
│   └── style.css             # Basic CSS
├── models/
│   └── database.py           # SQLite database models
├── routes/
│   ├── projects.py           # Project CRUD routes
│   ├── tasks.py              # Task CRUD routes
│   └── stories.py            # Live user story fetcher from GitHub API
└── tests/
    └── test_app.py           # Unit tests
```

---

## 4. README.md Requirements

Each repo must contain a README.md with:
- Project title and description
- Tech stack used
- How to run locally
- How to run via Docker
- API endpoint documentation
- Screenshots (add after development)
- Team member names and roles

---

## 5. Commit History Guidelines

Commits must follow this convention:
```
feat(US-04): add create project endpoint
fix(US-09): resolve task status update bug
docs: update README with docker instructions
ci: add Jenkins pipeline stage 3 for docker push
test: add unit tests for task routes
```

Each user story should have at least 2-3 commits showing incremental progress.
Minimum expected commits: **20+ commits** across the project lifecycle.

---

## 6. .gitignore Requirements

Must include exclusions for:
- Python: `__pycache__`, `*.pyc`, `.env`, `venv/`
- Database: `*.db`, `*.sqlite`
- IDE: `.vscode/`, `.idea/`
- Docker: no secrets committed
- OS: `.DS_Store`, `Thumbs.db`

---

## 7. Jenkinsfile / GitHub Actions Workflow

The pipeline must contain **at least 3 stages:**

| Stage | Name | Action |
|-------|------|--------|
| Stage 1 | Clone / Checkout | Clone the repository from GitHub |
| Stage 2 | Build & Test | Install dependencies and run unit tests |
| Stage 3 | Docker Build & Push | Build Docker image and push to DockerHub |
| Stage 4 *(Nice to Have)* | Deploy to EC2 | SSH into EC2, pull and run the Docker image |

---

## 8. Dockerfile Requirements

- Must be based on a lightweight official Python image (`python:3.11-slim`)
- Must install all dependencies from `requirements.txt`
- Must expose the correct application port
- Must start the Flask application on container run
- Final image should run with: `docker run -p 5000:5000 <dockerhub-username>/smarttrack-app`

---

## 9. DockerHub Image

- Create a public DockerHub repository named: `smarttrack-app`
- The CI/CD pipeline will automatically push images tagged with the Git commit SHA and `latest`
- **Test command after pulling:**
  ```bash
  docker pull <dockerhub-username>/smarttrack-app:latest
  docker run -p 5000:5000 <dockerhub-username>/smarttrack-app:latest
  # Visit http://localhost:5000 to verify the app runs
  ```

---

## 10. Nice to Have — AWS Deployment

### Steps:
1. **Register** a free AWS account at https://aws.amazon.com/free/
2. **Create an EC2 instance:**
   - AMI: Ubuntu Server 22.04 LTS (Free Tier eligible)
   - Instance type: `t2.micro`
   - Security Group: Allow ports 22 (SSH), 5000 (App), 8080 (Jenkins)
3. **Install Docker on EC2:**
   ```bash
   sudo apt update && sudo apt install docker.io -y
   sudo systemctl start docker
   sudo usermod -aG docker ubuntu
   ```
4. **Add Stage 4 to Jenkinsfile** to SSH into EC2, pull and run the Docker image
5. Store the EC2 private key as a Jenkins credential (ID: `ec2-ssh-key`)

---

## 11. Team Member Responsibilities (Suggested Split)

| Member | Responsibilities |
|--------|-----------------|
| Member 1 (You) | Flask API, Dockerfile, Database models, Jenkins/GitHub Actions pipeline |
| Member 2 | Frontend templates, Task routes, Unit tests |
| Member 3 | GitHub repo setup, DockerHub, EC2 setup, README documentation |

> Since you are completing this alone, commit using consistent author details and simulate the team structure through branch naming and PRs.

---

## 12. Submission Checklist

- [ ] GitHub repo is public and named `smarttrack-app`
- [ ] README.md is detailed and complete
- [ ] `.gitignore` covers all required exclusions
- [ ] At least 20 meaningful commits with proper messages
- [ ] Collaborators added to the repo (or documented)
- [ ] All PRs merged to `main` (no direct pushes)
- [ ] `Jenkinsfile` OR `.github/workflows/ci-cd.yml` present with 3+ stages
- [ ] `Dockerfile` builds and runs successfully
- [ ] Docker image pushed to DockerHub public repo
- [ ] `docker run` command executes the app successfully
- [ ] *(Nice to Have)* EC2 instance running with Stage 4 pipeline
- [ ] User stories documented in `user-stories.md` and trackable via GitHub Issues

---

*Generated for PSG DevOps Assignment | SmartTrack Application | 3-Member Team Project*
