# FastAPI + PostgreSQL + Docker

A FastAPI CRUD application with a PostgreSQL backend, demonstrating Docker Compose multi-container setup, Docker networking, named volumes for persistent data, and both manual Docker networking and Compose-based orchestration.

## 🚀 Features

- **Full CRUD API** — Create and list items with PostgreSQL persistence
- **Docker Compose** — Multi-container orchestration (FastAPI + PostgreSQL)
- **Named Volumes** — Persistent database storage across container restarts
- **Docker Networking** — Containers communicate via custom bridge network
- **Environment Configuration** — Database credentials via environment variables

## 📁 Project Structure

```
.
├── app.py                # FastAPI application with PostgreSQL
├── Dockerfile            # Container build instructions
├── compose.yaml          # Docker Compose multi-service config
└── commands.txt          # Manual Docker CLI commands reference
```

## 🛠️ Tech Stack

- **Python 3.9**
- **FastAPI** — High-performance API framework
- **PostgreSQL 15** — Relational database (Alpine image)
- **psycopg2** — PostgreSQL adapter for Python
- **Docker & Docker Compose** — Containerization and orchestration

## ⚡ Quick Start

### Option 1: Docker Compose (Recommended)

```bash
# Start both services
docker compose up --build -d

# Check logs
docker compose logs -f

# Stop everything
docker compose down
```

### Option 2: Manual Docker Commands

```bash
# Create network and volume
docker network create my-network
docker volume create pg_data

# Start PostgreSQL
docker run -d \
  --name postgres_container \
  --network my-network \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=secretpassword \
  -e POSTGRES_DB=testdb \
  -v pg_data:/var/lib/postgresql/data \
  postgres:15-alpine

# Build and start FastAPI
docker build -t db-app .
docker run -d \
  --name fastapi_container \
  --network my-network \
  -p 8000:8000 \
  -e DB_HOST=postgres_container \
  -e DB_NAME=testdb \
  -e DB_USER=postgres \
  -e DB_PASSWORD=secretpassword \
  db-app
```

### Test the API

```bash
# Home
curl http://localhost:8000/

# Create an item
curl -X POST http://localhost:8000/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "description": "A useful widget"}'

# List all items
curl http://localhost:8000/items/
```

## 📖 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Welcome message |
| POST | `/items/` | Create a new item |
| GET | `/items/` | List all items |

## 🗄️ Database Schema

The `items` table is auto-created on application startup:

| Column | Type | Constraints |
|--------|------|-------------|
| `id` | SERIAL | PRIMARY KEY |
| `name` | VARCHAR(100) | NOT NULL |
| `description` | TEXT | nullable |

## 📄 License

This project is open source and available under the [MIT License](LICENSE).
