# Browser Agent Context Enhancement - Server

> **Python FastAPI backend for browser agent context management**

This is the server application for the Browser Agent Context Enhancement project. It provides a REST API for browser automation agents with enhanced context management, memory capabilities, and Redis integration.

## 🎯 Overview

The server is a FastAPI application that provides:
- Browser automation capabilities using Browser Use
- Redis integration for context storage and caching
- RAG-indexed memory for semantic retrieval
- LangCache functionality for query trajectory caching
- API endpoints for browser agent operations

## 🛠️ Tech Stack

- **Framework**: FastAPI
- **Language**: Python 3.12+
- **Browser Automation**: Browser Use (`browser-use>=0.9.5`)
- **Package Management**: `uv` (modern Python package manager)
- **Server**: Uvicorn
- **Infrastructure**: Docker, Redis (planned)

## 📦 Installation

### Prerequisites

- Python 3.12+
- `uv` package manager (`pip install uv` or `brew install uv`)
- Redis server (to be added)

### Setup

1. Install dependencies:

```bash
cd server
uv sync
```

This will install all dependencies specified in `pyproject.toml` and create a virtual environment.

2. Create environment file (optional):

```bash
cp .env.example .env  # If you have an example file
# Or create .env manually
```

Add your Browser Use API key:

```env
BROWSER_USE_API_KEY=your_api_key_here
```

## 🚀 Development

### Start Development Server

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 4000 --reload
```

The API will be available at `http://localhost:4000`

### API Documentation

Once the server is running, you can access:
- **Interactive API docs**: `http://localhost:4000/docs` (Swagger UI)
- **Alternative docs**: `http://localhost:4000/redoc` (ReDoc)

### Health Check

```bash
curl http://localhost:4000/health
```

Expected response:
```json
{"status": "healthy"}
```

## 🐳 Docker

### Running with Docker Compose

From the project root:

```bash
docker-compose up
```

This will start the server with hot reload enabled. The server will be available at `http://localhost:4000`.

### Building Docker Image

```bash
docker build -t redis-hackathon-server .
```

### Running Docker Container

```bash
docker run -p 4000:4000 \
  -e BROWSER_USE_API_KEY=your_api_key \
  redis-hackathon-server
```

## 📁 Project Structure

```
server/
├── main.py              # FastAPI application entry point
├── pyproject.toml       # Python dependencies (uv)
├── uv.lock             # Locked dependencies
├── Dockerfile          # Docker container configuration
├── .env                # Environment variables (not in git)
└── README.md           # This file
```

## 🔌 API Endpoints

### Current Endpoints

- `GET /` - Root endpoint (returns welcome message)
  ```json
  {"message": "Hello from Redis hackathon server!"}
  ```

- `GET /health` - Health check endpoint
  ```json
  {"status": "healthy"}
  ```

### Planned Endpoints

- `POST /agent/execute` - Execute browser agent task
  - Request body: Task description and parameters
  - Response: Task execution results

- `POST /memory/store` - Store agent experience in long-term memory
  - Request body: Experience data, context, metadata
  - Response: Stored memory ID

- `GET /memory/search` - Semantic search over agent history (RAG)
  - Query parameters: Search query, limit, filters
  - Response: Relevant memories and context

- `GET /cache/query` - Retrieve cached query trajectories
  - Query parameters: Query pattern, similarity threshold
  - Response: Cached trajectories

- `POST /cache/store` - Store successful query trajectory
  - Request body: Query, trajectory, success metrics
  - Response: Cache key

- `GET /memory/history` - Retrieve agent interaction history
  - Query parameters: Limit, offset, filters
  - Response: Paginated interaction history

## 🎯 Features

### Implemented

- [x] FastAPI server setup with CORS middleware
- [x] Basic health check endpoint
- [x] Browser Use integration (dependency installed)
- [x] Docker support with hot reload
- [x] `uv` package management setup

### Planned

- [ ] **Redis Integration**: Connect to Redis server for data storage
- [ ] **RAG Indexed Memory**: Semantic search over historical interactions using Redis vector search
- [ ] **Long Term Memory**: Persistent storage of agent experiences and learnings
- [ ] **LangCache Implementation**: Redis-based caching layer for:
  - Storing previously successful query trajectories
  - Fast retrieval of similar queries and contexts
  - Pattern matching for recurring tasks
- [ ] **Browser Agent Execution**: Implement `/agent/execute` endpoint
- [ ] **Memory Management APIs**: Implement memory storage and retrieval endpoints
- [ ] **Redis Streams**: Integration for agent-to-agent communication
- [ ] **Redis Lane Cache**: Contextual memory management

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the server directory:

```env
# Browser Use API Key (required for browser automation)
BROWSER_USE_API_KEY=your_api_key_here

# Redis Configuration (to be added)
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_PASSWORD=
REDIS_DB=0

# Server Configuration
HOST=0.0.0.0
PORT=4000
DEBUG=true
```

### CORS Configuration

The server is configured to allow requests from `http://localhost:3000` (Next.js client). To modify CORS settings, edit `main.py`:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add more origins as needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## 📚 Dependencies

Current dependencies (from `pyproject.toml`):
- `browser-use>=0.9.5` - Browser automation library
- `fastapi>=0.120.4` - Web framework

Planned dependencies:
- `redis` - Redis Python client
- `redis-om` - Redis Object Mapping (optional)
- `langchain` - LangChain integration (optional)
- `langchain-redis` - LangChain Redis integration (optional)

## 🧪 Development Tips

### Using `uv`

- Install a new package: `uv add package-name`
- Install dev dependencies: `uv add --dev package-name`
- Sync dependencies: `uv sync`
- Run Python script: `uv run python script.py`
- Run command: `uv run command`

### Hot Reload

The server runs with `--reload` flag in development, which automatically restarts when code changes are detected.

### Virtual Environment

`uv` automatically manages the virtual environment. To activate it manually:

```bash
source .venv/bin/activate  # Linux/Mac
# or
.venv\Scripts\activate     # Windows
```

## 🐛 Troubleshooting

### Port Already in Use

If port 4000 is already in use:

```bash
uv run uvicorn main:app --host 0.0.0.0 --port 4001 --reload
```

### Browser Use API Key Issues

Make sure your `BROWSER_USE_API_KEY` is set correctly in your `.env` file or environment variables.

### Docker Issues

If you encounter issues with Docker:

1. Ensure Docker is running
2. Check Docker Compose logs: `docker-compose logs server`
3. Rebuild the container: `docker-compose build server`

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 📄 License

MIT

