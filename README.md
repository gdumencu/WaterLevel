# README.md
# WaterLevel Project
# WaterLevel Project

```markdown
# WaterLevel Project

**WaterLevel** is a telemetry system designed to monitor and visualize the movement of angle-controlled robots. It provides real-time tracking, deviation analysis, and projected arrival point visualization through a secure web dashboard.

---

## 🚀 Features

- Real-time UART data streaming and visualization
- Role-based access control (Admin, Operator, Viewer)
- Job configuration and robot path projection
- Audit logging and printable PDF reports
- Secure access over local network and internet
- Modular backend (FastAPI) and frontend (Next.js + TypeScript)

---

## 🧱 Project Structure

```
WaterLevel/
├── backend/       # FastAPI backend
├── frontend/      # Next.js frontend
├── docker-compose.yml
├── README.md
└── .gitignore
```

---

## ⚙️ Technologies

- **Backend**: FastAPI, SQLAlchemy, WebSockets, pyserial
- **Frontend**: Next.js, TypeScript, Recharts
- **Database**: PostgreSQL
- **Deployment**: Docker & Docker Compose

---

## 🛠️ Setup Instructions

### Prerequisites

- Python 3.10+
- Node.js 18+
- Docker Desktop
- Git & GitHub CLI
- VSCode (recommended)

### Clone the Repo

```bash
git clone https://github.com/gdumencu/WaterLevel.git
cd WaterLevel
```

### Run with Docker

```bash
docker-compose up --build
```

- Backend: http://localhost:8000
- Frontend: http://localhost:3000

---

## 📌 Development Workflow

1. Develop in small chunks (task-based)
2. Test locally
3. Commit to GitHub with descriptive messages
4. Push and continue

---

# WaterLevel Project – Environment Setup Checklist

## 1. Prerequisites
- [ ] Windows 10/11 with admin rights
- [ ] Internet access

## 2. Core Software
- [ ] Python 3.10+ (add to PATH)
- [ ] Node.js (LTS, e.g., 18.x+) and npm
- [ ] PostgreSQL (15+)
- [ ] Docker Desktop (enable WSL2 if prompted)
- [ ] Visual Studio Code
- [ ] Git

## 3. VSCode Extensions
- [ ] Python
- [ ] Pylance
- [ ] Docker
- [ ] Prettier
- [ ] ESLint
- [ ] GitHub Copilot (optional)

## 4. Project Repository
- [ ] Clone the repo: `git clone <repo-url>`
- [ ] Confirm backend and frontend folders exist
- [ ] Check `.gitignore` for secrets/build artifacts

## 5. Python Backend
- [ ] `cd backend`
- [ ] `python -m venv venv`
- [ ] `venv\Scripts\activate`
- [ ] `pip install -r requirements.txt`

## 6. Frontend
- [ ] `cd ../frontend`
- [ ] `npm install`
- [ ] Confirm `tsconfig.json` exists

## 7. Database
- [ ] Start PostgreSQL service
- [ ] Create database: `createdb waterlevel`
- [ ] (Optional) Set up initial tables

## 8. Docker
- [ ] Ensure Docker Desktop is running
- [ ] `docker-compose build`
- [ ] `docker-compose up`

## 9. GitHub Integration
- [ ] `gh auth login`
- [ ] Test push/pull

## 10. Documentation
- [ ] Update `README.md`
- [ ] Add onboarding checklist for new contributors

# Onboarding Guide

Welcome to the WaterLevel Telemetry Project!

## 1. Get Access
- Request access to the GitHub repo and SharePoint docs.
- Join project communication channels.

## 2. Set Up Your Environment
- Follow the Environment Setup Checklist above.
- For issues, check README troubleshooting or ask in team chat.

## 3. Understand the Project Structure
- Review backend, frontend, and shared config folders.
- Read the BRD and technical docs (see SharePoint links in README).

## 4. First Run
- Start PostgreSQL and Docker Desktop.
- Run backend and frontend locally (via Docker or directly).
- Open the dashboard in your browser and log in.

## 5. Development Workflow
- Create a new branch for your feature/bugfix.
- Commit changes with clear messages.
- Push to GitHub and open a pull request.
- Request code review.

## 6. Best Practices
- Use VSCode with recommended extensions.
- Keep `.env` files out of version control.
- Write clear, concise commit messages.
- Document new scripts or dependencies.

## 7. Support
- For onboarding help, contact the project lead or check the README.
- For technical issues, open a GitHub issue or ask in the team chat.


## 📄 License

This project is licensed for internal use and prototyping. Contact the author for deployment or commercial use.

---
## Troubleshooting
Runing scripta : Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
Remove permission: Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy Restricted


## 👤 Author

**Dorel Dumencu**  

