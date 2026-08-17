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
