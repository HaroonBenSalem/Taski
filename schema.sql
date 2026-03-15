-- Run this once to set up your database:
-- psql -U postgres -d your_db_name -f schema.sql

CREATE TABLE IF NOT EXISTS users (
    id        SERIAL PRIMARY KEY,
    email     VARCHAR(255) UNIQUE NOT NULL,
    password  VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS tasks (
    id         SERIAL PRIMARY KEY,
    user_id    INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task       VARCHAR(500) NOT NULL,
    priority   VARCHAR(10) NOT NULL DEFAULT 'medium',
    due_date   DATE,
    done       BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW()
);

-- Index so filtering by user_id is fast
CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id);
