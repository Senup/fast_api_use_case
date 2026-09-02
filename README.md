## FASTApi In and outs

This repo is used for learning fastapi, this would later pivot into a repo with a specific use case.

#### Features

- Task CRUD endpoints
- Request validation via Pydantic schemas
- Centralized error handling and logging
- Automated tests
---
#### Project structure

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

#### Prequisites - macos and ubuntu 
- Python (version number ?)
- uv

#### Steps to initiate the application

- `git clone <repository-url>`
- `cd fast_api_use_case/my-fastapi-app`
- `uv sync`

- `uv run fastapi dev app/main.py`

###### run the development server:

`uv run fastapi dev app/main.py`
- expected output will include a local URL similar to :
                                 
    - Swagger/OpenAPI UI: `http://127.0.0.1:8000/docs`
    - ReDoc documentation: `http://127.0.0.1:8000/redoc`
    - Raw OpenAPI specification: `http://127.0.0.1:8000/openapi.json`


#### Note:
Explanations of each and every code will be present in the hands_on.md 

---
This repository grows one practical FastAPI decision at a time: build it, break it, test it and understand why it works.
---

