# How to Run the ToDo List Project

## Prerequisites

- Python 3.12+
- Poetry (for dependency management)
- Docker and Docker Compose (for PostgreSQL database)

## Step-by-Step Setup

### 1. Install Dependencies

```bash
# Install Poetry if you haven't already
pip install poetry

# Install project dependencies
poetry install
```

### 2. Set Up Database

#### Start PostgreSQL with Docker:

```bash
# Start the database container
docker-compose up -d

# Verify it's running
docker ps
```

The database will be available at `localhost:5432` with:
- User: `todolist`
- Password: `todolist`
- Database: `todolist`

### 3. Configure Environment Variables

Create a `.env` file in the project root (copy from `.env.example`):

```bash
cp .env.example .env
```

### 4. Run Database Migrations

```bash
# Run Alembic migrations to create tables
poetry run alembic upgrade head
```

This will create the `projects` and `tasks` tables in the database.

### 5. Run the Main Application

```bash
# Using Poetry
poetry run python -m src.main
```

## Using Commands

### Autoclose Overdue Tasks

Manually run the autoclose command:

```bash
# Using Poetry
poetry run todolist tasks:autoclose-overdue

# OR directly
poetry run python -m src.cli tasks:autoclose-overdue
```

This will find all tasks where:
- `deadline < today`
- `status != "done"`

And automatically mark them as done with a `closed_at` timestamp.

### Set Up Automated Scheduler

The scheduler can run automatically as a system service (recommended) or manually.

#### Option 1: Automatic Startup (Recommended - Linux)

Install as a systemd service for automatic startup:

```bash
# Install the service
./scripts/install-scheduler-service.sh

# Start the service
systemctl --user start todolist-scheduler

# Enable auto-start on boot
systemctl --user enable todolist-scheduler

# Check status
systemctl --user status todolist-scheduler

# View logs
journalctl --user -u todolist-scheduler -f
```

The scheduler will:
- Start automatically on system boot
- Run autoclose-overdue daily at midnight (00:00)
- Restart automatically if it crashes
- Log to `~/.todo-list/scheduler.log` and systemd journal

#### Option 2: Manual Run

To run the scheduler manually (for testing or if systemd is not available):

```bash
# Using Poetry
poetry run todolist scheduler:run

# OR directly
poetry run python -m src.cli scheduler:run
```

The scheduler will:
- Run autoclose-overdue daily at midnight (00:00)
- Check for pending tasks every minute
- Run continuously until stopped (Ctrl+C)
- Log to `~/.todo-list/scheduler.log`

## Troubleshooting

### Database Connection Issues

If you get connection errors:

1. **Check if Docker container is running:**
   ```bash
   docker ps
   docker-compose ps
   ```

2. **Check database logs:**
   ```bash
   docker-compose logs postgres
   ```

3. **Restart the database:**
   ```bash
   docker-compose restart postgres
   ```

4. **Verify .env file exists and has correct values**

### Migration Issues

If migrations fail:

1. **Check current migration status:**
   ```bash
   poetry run alembic current
   ```

2. **View migration history:**
   ```bash
   poetry run alembic history
   ```

3. **Reset database (⚠️ WARNING: This deletes all data):**
   ```bash
   docker-compose down -v
   docker-compose up -d
   poetry run alembic upgrade head
   ```

## Stopping the Database

When you're done:

```bash
# Stop the database container
docker-compose down

# Stop and remove volumes (⚠️ deletes all data)
docker-compose down -v
```

## Quick Start Summary

```bash
# 1. Install dependencies
poetry install

# 2. Start database
docker-compose up -d

# 3. Create .env file
cp .env.example .env

# 4. Run migrations
poetry run alembic upgrade head

# 5. Run the application
poetry run python -m src.main
```
