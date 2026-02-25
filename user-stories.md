# SmartTrack — User Stories
> These stories are also tracked as GitHub Issues (label: `user-story`) and fetched live by the application at `/api/stories`

## How to add these to GitHub Issues

1. Go to your repo → Issues → New Issue
2. Add title exactly as shown below
3. Add label: `user-story`
4. Add label for priority: `High`, `Medium`, or `Low`

---

## Epic 1: User & Authentication
- **US-01** | As a user, I want to register with name, email, and password | `High`
- **US-02** | As a user, I want to log in and receive a session token | `High`
- **US-03** | As an admin, I want to manage team members | `Medium`

## Epic 2: Project Management
- **US-04** | As a user, I want to create a new project with a name and description | `High`
- **US-05** | As a user, I want to view all projects I am a member of | `High`
- **US-06** | As a user, I want to delete a project I own | `Medium`
- **US-07** | As a user, I want to assign team members to a project | `Medium`

## Epic 3: Task Management
- **US-08** | As a user, I want to create tasks with title, assignee, and priority | `High`
- **US-09** | As a user, I want to update task status (Todo / In Progress / Done) | `High`
- **US-10** | As a user, I want to filter tasks by status or assignee | `Medium`
- **US-11** | As a user, I want to set a due date for tasks | `Medium`
- **US-12** | As a user, I want to delete tasks that are no longer relevant | `Low`

## Epic 4: Dashboard & Reporting
- **US-13** | As a user, I want a dashboard with task completion stats per project | `High`
- **US-14** | As a user, I want a visual chart of tasks by priority | `Medium`
- **US-15** | As a user, I want live user stories fetched from GitHub Issues | `Medium`

## Epic 5: DevOps & Deployment
- **US-16** | As a developer, I want the app containerized with Docker | `High`
- **US-17** | As a developer, I want a Jenkins/GitHub Actions pipeline with 3+ stages | `High`
- **US-18** | As a developer, I want the Docker image pushed to DockerHub | `High`
- **US-19** | As a DevOps engineer, I want Stage 4 to deploy to AWS EC2 | `Nice to Have`
