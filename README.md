# ToDo List API

A RESTful API for managing projects and tasks, built with FastAPI.

> ⚠️ **DEPRECATION NOTICE**: The CLI interface is deprecated and will be removed in a future version. Please use the Web API instead.

## Features

* **RESTful API**: Full CRUD operations for projects and tasks
* **Automatic Documentation**: Swagger UI at `/docs` and ReDoc at `/redoc`
* **Data Validation**: Pydantic-based request/response validation
* **PostgreSQL**: Persistent storage with SQLAlchemy ORM
* **Database Migrations**: Alembic for schema management

## Getting Started

### Prerequisites

* Python 3.12+
* Docker (for PostgreSQL)
* Poetry

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/ykazemim/todo-list.git
   cd todo-list
   ```

2. **Install dependencies:**
   ```bash
   pip install poetry
   poetry install
   ```

3. **Set up environment:**
   ```bash
   cp .env.example .env
   ```

4. **Start PostgreSQL:**
   ```bash
   docker compose up -d
   ```

5. **Run database migrations:**
   ```bash
   poetry run alembic upgrade head
   ```

### Running the API

```bash
poetry run uvicorn src.api.app:app --reload
```

The API will be available at `http://localhost:8000`.

* **Swagger UI**: http://localhost:8000/docs
* **ReDoc**: http://localhost:8000/redoc

### API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/projects` | List all projects |
| POST | `/api/v1/projects` | Create a project |
| GET | `/api/v1/projects/{id}` | Get a project |
| PUT | `/api/v1/projects/{id}` | Update a project |
| DELETE | `/api/v1/projects/{id}` | Delete a project |
| GET | `/api/v1/projects/{id}/tasks` | List tasks in a project |
| POST | `/api/v1/projects/{id}/tasks` | Create a task |
| GET | `/api/v1/projects/{id}/tasks/{task_id}` | Get a task |
| PUT | `/api/v1/projects/{id}/tasks/{task_id}` | Update a task |
| PATCH | `/api/v1/projects/{id}/tasks/{task_id}/status` | Change task status |
| DELETE | `/api/v1/projects/{id}/tasks/{task_id}` | Delete a task |

### CLI (Deprecated)

The CLI is deprecated but still available:

```bash
poetry run python src/main.py
```

### Scheduled Tasks

Auto-close overdue tasks:
```bash
poetry run todolist tasks:autoclose-overdue
```

Run the scheduler daemon:
```bash
poetry run todolist scheduler:run
```

## Contributing

Contributions are welcome! Please submit pull requests.

## License

MIT License. See [LICENSE](LICENSE) for details.
