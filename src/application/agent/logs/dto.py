from datetime import datetime
from pydantic import BaseModel

class LogPayload(BaseModel):
    """Model for agent log upload payload."""
    task_id: str
    agent_id: str
    exit_code: int
    stdout: str
    stderr: str
    execution_time_ms: int
    completed_at: datetime
