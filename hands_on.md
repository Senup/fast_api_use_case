#### Hands-on Documentation

### Set up the FastAPI porject with uv 

- initialize uv 

`uv init --bare`  
- This will create the python project metadata 

`uv add "fastapi[standard]"` 

- add FastAPI to pyproject.toml
- add the required development server dependencies 
- create or update uv.lock
- create a local .venv environment when needed

`uv sync`
`uv run python --version`

