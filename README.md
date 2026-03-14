# MedAudit: AI-Powered Medical Bill & Prescription Analyzer

An intelligent system that analyzes prescriptions, detects billing fraud, parses insurance policies, and tracks health metrics over time.

## Features
- 💊 Drug prescription analysis with insurance coverage
- 📋 Hospital bill fraud detection & cost breakdown
- 📊 Health wallet with lab report trends
- 📄 Insurance policy parsing & breakdown
- 🎙️ Doctor consultation management

## Quick Start (No Docker needed)

### Prerequisites
- Python 3.11+
- Node.js 18+

### 1. Add your API key

Edit `.env` and set your Claude API key:

```
CLAUDE_API_KEY=sk-ant-...
```

### 2. Run

```bash
./start.sh
```

That's it. The script will:
- Create a Python virtual environment automatically
- Install all backend & frontend dependencies
- Start both servers

### Access
| Service  | URL |
|----------|-----|
| Frontend | http://localhost:5173 |
| Backend  | http://localhost:8000 |
| API Docs | http://localhost:8000/docs |

The SQLite database is created automatically at `backend/medaudit.db` — no database setup required.

Press **Ctrl+C** to stop everything.

---

## Tech Stack
- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python 3.11
- **Database:** SQLite (zero config) — swap to PostgreSQL via `DATABASE_URL` in `.env`
- **AI:** Claude API

## Project Structure

```
medaudit/
├── start.sh          ← run this
├── .env              ← add your API key here
├── backend/          # FastAPI application
│   ├── app/
│   │   ├── main.py
│   │   ├── config.py
│   │   ├── models/
│   │   ├── services/
│   │   └── api/routes/
│   └── requirements.txt
└── frontend/         # React application
    └── src/
```

## Docker (optional)

If you prefer Docker:

```bash
docker-compose up
```

Built for GenAI Genesis 2026 Hackathon
