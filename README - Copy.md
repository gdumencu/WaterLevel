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

## 📄 License

This project is licensed for internal use and prototyping. Contact the author for deployment or commercial use.

---

## 👤 Author

**Dorel Dumencu**  

