import uuid
import json
from typing import Optional, List, Dict, Any
from datetime import datetime, timezone
from domain.aggregate.agent.agent_repository import AgentRepository
# Assuming SQLiteRepository and CloudflareKVRepo are available and have necessary methods
from infrastructure.database.impl_sqlite_repository import SQLiteRepository
from infrastructure.cloudflare_kv.impl_cloudflare_kv_repository import CloudflareKVRepo
from src.config import Settings # Import settings

# Helper to convert datetime to ISO format string for KV
def datetime_to_iso(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.isoformat()

# Helper to parse ISO format string to datetime
def iso_to_datetime(iso_str: str) -> datetime:
    return datetime.fromisoformat(iso_str.replace('Z', '+00:00'))

class AgentRepositoryImpl(AgentRepository):
    def __init__(self, db_repo: SQLiteRepository, kv_repo: CloudflareKVRepo, settings: Settings):
        self.db = db_repo # SQLite repository instance
        self.kv = kv_repo # Cloudflare KV repository instance
        self.settings = settings # Application settings

    async def create_task(self, command: str, timeout: int, upload_log: bool) -> str:
        task_id = str(uuid.uuid4())
        task_data = {
            "task_id": task_id,
            "command_string": command,
            "timeout_seconds": timeout,
            "upload_log": upload_log,
            "working_directory": ".", # Placeholder
            "created_at": datetime_to_iso(datetime.utcnow()), # Assuming created_at is needed
            "status": "pending" # Assuming a status field
        }

        if self.settings.DB_ENGINE == "sqlite":
            query = """
            INSERT INTO tasks (task_id, command_string, timeout_seconds, upload_log, working_directory, created_at, status)
            VALUES (:task_id, :command_string, :timeout_seconds, :upload_log, :working_directory, :created_at, :status)
            """
            await self.db.execute(query, task_data)
        elif self.settings.DB_ENGINE == "cloudflare_kv":
            # Store task details with task_id as key
            await self.kv.put(f"task:{task_id}", json.dumps(task_data))
            # Optional: Store a secondary index for fetching by agent if needed later
            # await self.kv.put(f"agent_task:{agent_id}:{task_id}", "")
        else:
            raise ValueError(f"Unsupported DB_ENGINE: {self.settings.DB_ENGINE}")
        return task_id

    async def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        if self.settings.DB_ENGINE == "sqlite":
            query = "SELECT * FROM tasks WHERE task_id = :task_id"
            params = {"task_id": task_id}
            result = await self.db.fetch_one(query, params)
            return result
        elif self.settings.DB_ENGINE == "cloudflare_kv":
            task_data_str = await self.kv.get(f"task:{task_id}")
            if task_data_str:
                return json.loads(task_data_str)
            return None
        else:
            raise ValueError(f"Unsupported DB_ENGINE: {self.settings.DB_ENGINE}")

    async def store_log(self, task_id: str, agent_id: str, exit_code: int,
                      stdout: str, stderr: str, exec_time_ms: int) -> None:
        log_data = {
            "task_id": task_id,
            "agent_id": agent_id,
            "exit_code": exit_code,
            "stdout": stdout,
            "stderr": stderr,
            "execution_time_ms": exec_time_ms,
            "completed_at": datetime_to_iso(datetime.utcnow())
        }

        if self.settings.DB_ENGINE == "sqlite":
            query = """
            INSERT INTO logs (task_id, agent_id, exit_code, stdout, stderr, execution_time_ms, completed_at)
            VALUES (:task_id, :agent_id, :exit_code, :stdout, :stderr, :execution_time_ms, :completed_at)
            """
            await self.db.execute(query, log_data)
            # Optional: Update task status to 'completed' in tasks table
            # update_task_query = "UPDATE tasks SET status = 'completed' WHERE task_id = :task_id"
            # await self.db.execute(update_task_query, {"task_id": task_id})
        elif self.settings.DB_ENGINE == "cloudflare_kv":
            # Store log details with a key structure that links to task and agent
            log_key = f"log:{task_id}:{agent_id}" # Example key structure
            await self.kv.put(log_key, json.dumps(log_data))
            # Optional: Update task status in KV
            # task_key = f"task:{task_id}"
            # task_data_str = await self.kv.get(task_key)
            # if task_data_str:
            #     task_data = json.loads(task_data_str)
            #     task_data['status'] = 'completed'
            #     await self.kv.put(task_key, json.dumps(task_data))
        else:
            raise ValueError(f"Unsupported DB_ENGINE: {self.settings.DB_ENGINE}")

    async def get_pending_tasks_for_agent(self, agent_id: str, since: datetime) -> List[Dict[str, Any]]:
        if self.settings.DB_ENGINE == "sqlite":
            # Refined query: Select tasks created since 'since' that do NOT have a corresponding log entry
            # and are linked to the agent (assuming agent_id is stored with the task or can be inferred)
            # Assuming tasks table has 'created_at' and 'agent_id' columns (needs migration update)
            query = """
            SELECT t.* FROM tasks t
            LEFT JOIN logs l ON t.task_id = l.task_id
            WHERE l.task_id IS NULL -- Task has no corresponding log entry (assuming pending means no log)
            AND t.agent_id = :agent_id -- Assuming tasks are assigned to agents
            AND t.created_at >= :since -- Filter by creation time
            """
            params = {"agent_id": agent_id, "since": since}
            # This query assumes schema changes (agent_id, created_at in tasks table)
            results = await self.db.fetch_all(query, params)
            return results
        elif self.settings.DB_ENGINE == "cloudflare_kv":
            # Fetching pending tasks for a specific agent since a timestamp in KV is complex.
            # A simple approach is to list keys and filter, but this can be inefficient.
            # Assuming tasks are stored with a key like "task:{task_id}" and have a 'status' and 'created_at' field.
            # A more robust KV design might involve secondary indexes or different key structures.
            # For this implementation, I'll simulate by listing all tasks and filtering in memory (inefficient for large data).
            # A better KV approach might involve storing pending task IDs under an agent-specific key.
            all_tasks_keys = await self.kv.list_keys("task:") # Assuming list_keys with prefix is available
            pending_tasks = []
            for key in all_tasks_keys:
                task_data_str = await self.kv.get(key)
                if task_data_str:
                    task_data = json.loads(task_data_str)
                    # Assuming task_data includes 'agent_id', 'status', and 'created_at'
                    if (task_data.get("agent_id") == agent_id and
                        task_data.get("status") == "pending" and
                        iso_to_datetime(task_data.get("created_at")) >= since):
                        pending_tasks.append(task_data)
            return pending_tasks
        else:
            raise ValueError(f"Unsupported DB_ENGINE: {self.settings.DB_ENGINE}")
        return []
