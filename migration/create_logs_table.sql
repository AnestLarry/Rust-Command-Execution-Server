CREATE TABLE logs (
    task_id VARCHAR(255),
    agent_id VARCHAR(255),
    exit_code INTEGER NOT NULL,
    stdout TEXT,
    stderr TEXT,
    execution_time_ms INTEGER NOT NULL,
    completed_at DATETIME NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(task_id)
);
