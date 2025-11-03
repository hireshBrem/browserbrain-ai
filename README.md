# BrowserBrain AI

> **95x FASTER with cache for browser agent tasks**

Browserbrain AI implements a semantic context caching layer for browser agents.

## 🎯 Why?

Browser agents are slow and expensive. They struggle with doing the same task again even though it did in 100 times in a row!?!

## 🚀 Solution

This project combines **Browser Use** (browser automation library) with **Redis** to provide:
- **LangCache from Redis**: Fast retrieval of previously successful query trajectories and similar contexts

## 🏗️ Architecture

### System Architecture Diagram

![Context Engineering Architecture](./architecture.png)

Our architecture implements a sophisticated three-tier context engineering system designed to overcome LLM context limitations and enable truly autonomous browser agents with persistent memory.

### Architecture Layers

#### 1. Context Layer

The **Context Layer** provides persistent, intelligent memory storage for tasks that transcends simple browser agents.

#### 2. Browser Agent Layer

The **Browser Agent Layer** executes tasks autonomously. Browser use package we use can be customised; add built-in tools and custom tools.  

## 🛠️ Tech Stack

- **Backend**: Python 3.12+, FastAPI, Browser Use, Redis, uvicorn, Langcache
- **Frontend**: Next.js 16, React 19, TypeScript, Tailwind CSS
- **Infrastructure**: Docker, Docker Compose
- **Package Management**: `uv` for Python dependencies

## 📦 Installation & Setup

### Prerequisites

- Docker & Docker Compose
- Set up environment variables

### Installing Dependencies

#### Backend (Python)

Navigate to the server directory and install Python dependencies using `uv`:

```bash
cd server
uv sync
```

#### Frontend (Next.js)

Navigate to the client directory and install Node dependencies:

```bash
cd client
npm install
```

### Running the Project



Start all services:
```bash
docker compose watch
```

Rebuild containers before starting:
```bash
docker compose build
```

Stop services:
```bash
docker compose down
```

Stop and remove volumes:
```bash
docker compose down -v
```

View logs in realtime:
```bash
docker compose logs -f
```


## 📊 Speed Benchmark: Cache vs Agent Execution

Test how much faster cached responses are compared to creating new browser agent tasks.

### Running the Benchmark (do it yourself!!!)

```bash
cd server
uv run test_speed_benchmark.py
```

### Example Results

```
============================================================
RESULTS
============================================================

Agent Execution Time:  14.13 seconds
Avg Cache Retrieval:   149.24ms

Speedup:               95x faster with cache
Time Saved Per Query:  13.98 seconds

============================================================
```

This demonstrates the **95x speedup** achieved through semantic caching with LangCache - transforming seconds of agent execution into milliseconds of cache retrieval.

## 🤝 Contributing

This is a hackathon project. Contributions welcome!

## 🤙 Contact
> GitHub [@hireshb](https://github.com/hireshb) &nbsp;&middot;&nbsp;
> Twitter [@hiresh_b](https://x.com/hiresh_b)