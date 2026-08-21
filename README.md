# FastAPI Learning Summary — Issues #50 to #54

This document summarizes the code written so far while building a small Task REST API.

> Current scope: project setup, FastAPI application, health check, Pydantic schemas, tests, and in-memory task creation/listing.
>
> Not built yet: retrieving one task, updating, deleting, database storage, authentication, authorization, or production deployment.

---

## 1. Project structure

Current relevant structure:

```text
my-fastapi-app/
├── api/
│   └── tasks.py
├── schemas/
│   └── task.py
├── tests/
│   ├── test_health.py
│   ├── test_task_schemas.py
│   └── test_tasks.py
├── main.py
├── pyproject.toml
└── uv.lock
```
-- Chief will take the documentation 
`curl -LsSf https://astral.sh/uv/install.sh | sh`
---
`uv --version`
---
`uv init my-fastapi-app --no-package`
---
`cd my-fastapi-app`
---
`uv add "fastapi[standard]"`
---

`from fastapi import FastAPI`
---
`app = FastAPI()`
----
`@app.get("/")`
`def read_root():`
    `return {"message": "Hello from FastAPI powered by uv!"}`
---
`uv run fastapi dev main.py`
---
`git ls-files | grep -E "\.env|\.venv|__pycache__"`
---

Adding the first automated API test and estatbilish the test command for the repo

`mkdir -p tests`
`touch tests/__init__.py`
