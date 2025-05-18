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

2. Configure environment variables. Copy one of the example files (`.env.sqlite.example` or `.env.cfkv.example`) to `.env` and update the values.

   - `DB_ENGINE`: Specifies the database engine. Use `sqlite` for SQLite or `cloudflare_kv` for Cloudflare KV.
   - `DB_URL`: Database connection URL (required for `sqlite`).
   - Cloudflare KV settings (`CF_ACCOUNT_ID`, `CF_KV_NAMESPACE_ID`, `CF_API_TOKEN`) are required when `DB_ENGINE` is `cloudflare_kv`.
   - `CORS_ORIGINS`: List of allowed CORS origins.

   Example `.env` for SQLite:
   ```ini
   DB_ENGINE=sqlite
   DB_URL=sqlite:///./rces.db
   CORS_ORIGINS=["*"]
   ```

   Example `.env` for Cloudflare KV:
   ```ini
   DB_ENGINE=cloudflare_kv
   CF_ACCOUNT_ID=your_cloudflare_account_id
   CF_KV_NAMESPACE_ID=your_cloudflare_kv_namespace_id
   CF_API_TOKEN=your_cloudflare_api_token
   CORS_ORIGINS=["*"]
   ```

3. Run the server:
```bash
uvicorn src.main:app --reload
