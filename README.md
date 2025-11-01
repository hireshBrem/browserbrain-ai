# Browser Agent Context Enhancement

> **10x memory for browser agents**

Browser agents suffer from poor context retention and memory limitations. This project addresses that by leveraging Redis to provide enhanced context management and memory capabilities for browser automation agents.

## 🎯 Problem

Browser agents have trash context. They struggle with:
- Limited memory retention across sessions
- Inefficient context management
- Poor state persistence
- Context loss between interactions

## 🚀 Solution

This project combines **Browser Use** (browser automation library) with **Redis** to provide:
- Persistent context storage
- Enhanced memory capabilities
- Improved state management
- Better context retention across sessions

## 🏗️ Architecture

### Components

- **Server** (`/server`): Python FastAPI backend
  - Uses `browser-use` for browser automation
  - Integrates with Redis for context storage
  - Provides API endpoints for browser agent operations

- **Client** (`/client`): Next.js frontend (planned)
  - Web interface for interacting with browser agents
  - Visualize context and memory management

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Browser Use, Redis
- **Frontend**: Next.js (planned)
- **Infrastructure**: Docker, Docker Compose

## 📦 Installation

### Prerequisites

- Python 3.12+
- Redis server
- Docker & Docker Compose (optional)

### Server Setup

```bash
cd server
uv sync
```

### Running with Docker Compose

```bash
docker-compose up
```

## 🚦 Getting Started

### Start the Server

```bash
cd server
uvicorn main:app --reload
```

The API will be available at `http://localhost:8000`

### Health Check

```bash
curl http://localhost:8000/health
```

## 📝 API Endpoints

- `GET /` - Root endpoint
- `GET /health` - Health check endpoint

## 🎯 Features

- [x] Basic FastAPI server setup
- [x] Browser Use integration
- [ ] Redis context storage
- [ ] Enhanced memory management
- [ ] Next.js frontend (planned)

## 📚 Project Structure

```
redis-hackathon/
├── server/          # FastAPI backend
│   ├── main.py     # Application entry point
│   └── pyproject.toml
├── client/          # Next.js frontend (planned)
└── docker-compose.yml
```

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT
