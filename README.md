# MedAudit: AI-Powered Medical Bill & Prescription Analyzer

An intelligent system that analyzes prescriptions, detects billing fraud, parses insurance policies, transcribes doctor consultations, and tracks health metrics over time.

## Features
- 💊 Drug prescription analysis with insurance coverage
- 📋 Hospital bill fraud detection & cost breakdown
- 🎙️ Real-time doctor consultation transcription
- 📊 Health wallet with lab report trends
- 📄 Insurance policy parsing & breakdown

## Quick Start

### Prerequisites
- Docker & Docker Compose
- Git

### Setup

```bash
# Clone repo
git clone <your-repo>
cd medaudit

# Copy environment file
cp .env.example .env
# Edit .env with your API keys

# Start all services
docker-compose up

# Access:
# Frontend: http://localhost:5173
# Backend: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

## Tech Stack
- **Frontend:** React 18 + TypeScript + Tailwind CSS
- **Backend:** FastAPI + Python 3.11
- **Database:** PostgreSQL + Redis
- **AI:** Claude API, Whisper API

## Project Structure

```
medaudit/
├── backend/          # FastAPI application
├── frontend/         # React application
├── docker-compose.yml
├── .env.example
└── README.md
```

## API Documentation
Once running, visit: http://localhost:8000/docs

Built for GenAI Genesis 2026 Hackathon
