# Rust Command Execution Server (RCES)

FastAPI server for managing agent commands and execution logs.

## Features

- REST API for agent communication
- Database engine switching via environment variables
- DDD architecture pattern
- Async database operations

## API Endpoints

### GET /api/v1/agent/commands
Fetch pending commands for an agent

**Parameters:**
- `agent_id` (required): Agent identifier
- `since` (optional): Filter commands since timestamp

**Response:**
```json
{
  "server_current_time": "ISO8601 timestamp",
  "tasks": [
    {
      "task_id": "string",
      "command_string": "string",
      "timeout_seconds": 0,
      "upload_log": true,
      "working_directory": "string|null"
    }
  ]
}
```

### POST /api/v1/agent/logs
Upload execution logs from an agent

**Request Body:**
```json
{
  "task_id": "string",
  "agent_id": "string",
  "exit_code": 0,
  "stdout": "string",
  "stderr": "string",
  "execution_time_ms": 0,
  "completed_at": "ISO8601 timestamp"
}
```

## Setup

1. Install dependencies:
```bash
uv pip install -e .
```

2. Configure environment variables in `.env`:
```ini
DB_ENGINE=sqlite|postgres
DB_URL=your_database_url
```

3. Run the server:
```bash
uvicorn src.main:app --reload
