from datetime import datetime
from pydantic import BaseModel
from typing import List, Optional

class ServerTask(BaseModel):
    """Model for individual server task."""
    task_id: str
    command_string: str
    timeout_seconds: int
    upload_log: bool
    working_directory: Optional[str] = None

class FetchTasksResponse(BaseModel):
    """Model for fetch tasks response."""
    server_current_time: datetime
    tasks: List[ServerTask]
