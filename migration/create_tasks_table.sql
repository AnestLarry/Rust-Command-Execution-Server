CREATE TABLE tasks (
    task_id VARCHAR(255) PRIMARY KEY,
    command_string TEXT NOT NULL,
    timeout_seconds INTEGER NOT NULL,
    upload_log BOOLEAN NOT NULL,
    working_directory VARCHAR(255)
);
