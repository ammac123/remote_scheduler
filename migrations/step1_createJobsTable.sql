CREATE TABLE jobs (
    job_id INTEGER PRIMARY KEY,
    job_name VARCHAR(50) NOT NULL,
    trigger_type VARCHAR(100),
    next_trigger_time DATETIME
);