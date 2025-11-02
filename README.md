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
- **RAG Indexed Memory**: Semantic search over historical interactions and context
- **Long Term Memory**: Persistent storage of agent experiences and learnings
- **LangCache from Redis**: Fast retrieval of previously successful query trajectories and similar contexts
- Persistent context storage across sessions
- Enhanced state management for browser automation

## 🏗️ Architecture

### Components

- **Server** (`/server`): Python backend (using `uv`)
  - Uses `browser-use` for browser automation
  - Integrates with Redis for context storage and caching
  - Implements RAG-indexed memory for semantic retrieval
  - Provides LangCache functionality for query trajectory caching
  - Provides API endpoints for browser agent operations

- **Client** (`/client`): Next.js frontend
  - Web interface for interacting with browser agents
  - Visualize context and memory management
  - Real-time interaction with the browser automation API

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Browser Use, Redis, uvicorn
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose
- **Package Management**: `uv` for Python dependencies

## 📦 Installation

### Prerequisites

- Python 3.12+
- Node.js 20+ (for client)
- Redis server (to be added)
- Docker & Docker Compose (optional)
- `uv` package manager (`pip install uv` or `brew install uv`)

### Server Setup

```bash
cd server
uv sync
```

### Client Setup

```bash
cd client
npm install
```

### Running with Docker Compose

```bash
docker-compose up
```

This will start:
- **Server**: `http://localhost:4000`
- **Client**: `http://localhost:3000`

## 🚦 Getting Started

### Start the Server

```bash
cd server
uv run uvicorn main:app --host 0.0.0.0 --port 4000 --reload
```

The API will be available at `http://localhost:4000`

### Start the Client

```bash
cd client
npm run dev
```

The client will be available at `http://localhost:3000`

### Health Check

```bash
curl http://localhost:4000/health
```

## 📝 API Endpoints

### Current Endpoints
- `GET /` - Root endpoint (returns welcome message)
- `GET /health` - Health check endpoint

### Planned Endpoints
- `POST /agent/execute` - Execute browser agent task
- `POST /memory/store` - Store agent experience in long-term memory
- `GET /memory/search` - Semantic search over agent history (RAG)
- `GET /cache/query` - Retrieve cached query trajectories
- `POST /cache/store` - Store successful query trajectory
- `GET /memory/history` - Retrieve agent interaction history

## 🎯 Features

### Implemented
- [x] Basic FastAPI server setup with CORS middleware
- [x] Browser Use integration
- [x] Next.js frontend application
- [x] Docker Compose setup with hot reload
- [x] Development environment configuration

### Planned
- [ ] **RAG Indexed Memory**: Semantic search over historical interactions and context using Redis vector search
- [ ] **Long Term Memory**: Persistent storage of agent experiences, learnings, and state across sessions
- [ ] **LangCache Implementation**: Redis-based caching layer for:
  - Storing previously successful query trajectories
  - Fast retrieval of similar queries and contexts
  - Pattern matching for recurring tasks
- [ ] Redis Streams integration for agent-to-agent communication
- [ ] Redis Lane Cache for contextual memory management
- [ ] Enhanced memory management and retrieval APIs

## 📚 Project Structure

```
redis-hackathon/
├── server/                  # Python FastAPI backend
│   ├── main.py             # Application entry point
│   ├── pyproject.toml      # Python dependencies (uv)
│   ├── uv.lock            # Locked dependencies
│   ├── Dockerfile          # Server container config
│   └── README.md           # Server documentation
├── client/                  # Next.js frontend
│   ├── src/
│   │   └── app/           # Next.js app directory
│   ├── package.json        # Node.js dependencies
│   ├── Dockerfile          # Client container config
│   └── README.md           # Client documentation
├── docker-compose.yml      # Multi-container orchestration
├── project                 # Project idea and features
└── README.md               # This file
```

## 🏆 Hackathon Goals

This project is designed for the Redis Hackathon and focuses on:

- **Technical Execution**: Deep integration with Redis core datatypes (Streams, Lane Cache, etc.)
- **Creativity & Impact**: Novel approach to browser agent memory management
- **Builder Clarity**: Clear architecture and context design documentation
- **Polish & Presentation**: Working demo with comprehensive documentation

## 🔮 Future Enhancements

- Redis Streams for A2A communication between autonomous agents
- Redis Pub/Sub for real-time agent coordination
- Integration with LangChain, LlamaIndex, or Composio frameworks
- Advanced vector search capabilities
- Multi-modal workflow support

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT
