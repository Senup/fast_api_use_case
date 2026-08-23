#### Hands-on Documentation

### Set up the FastAPI project with uv 

- initialize uv 

`uv init --bare`  
- This will create the python project metadata 

`uv add "fastapi[standard]"` 

- add FastAPI to pyproject.toml
- add the required development server dependencies 
- create or update uv.lock
- create a local .venv environment when needed (check if we really need venv if we are using uv)

`uv sync`
`uv run python --version`

`git status`
<  paste the output here >

### Create the FastAPI application and health endpoint:

#### creating the application package 


`mkdir -p app`
`touch app/__init__.py`

- create the FastAPI entry point in  app/main.py
- `@app.get("/health")` registers a GET route
- `/health` is a resource independent operationsal endpoint, it does not belong under /api/v1..
- FastAPI converts the returned python dict into JSON automatically
- The return type hine describes the response shape
- `tags=["Health"]` groups the route in Swagger UI

#### run the development server

`uv run fastapi dev app/main.py`

- expected output will include a local URL similar to :
                                    
- Open 
    - Swagger/OpenAPI UI: `http://127.0.0.1:8000/docs`
    - ReDoc documentation: `http://127.0.0.1:8000/redoc`
    - Raw OpenAPI specification: `http://127.0.0.1:8000/openapi.json`

### Adding automated tests for health endpoint 

`uv add --dev pytest httpx`
- pytests discovers and run tests
- httpx sends HTTP requests to the FastAPI in tests

#### Create the tests directory 

- mkdir -p tests
- touch tests/__init__.py

#### Add the health endpoint test 
- Health endpoint: `http://127.0.0.1:8000` and it contains `{"status"="ok"}`

### Defining the Pydantic schemas for tasks

#### Create the schemas package

`mkdir -p schemas`

- `TaskCreate` is the incoming create-request
- `TaskUpdate` makes the field optional because `Patch` updates only the fields a client sends
- `TaskResponse` is the outgoing API contract. Client cannot choose an id or timestamps
- `StrEnum` restricts `status` and `priority` to known values while still serializing as normal JSON strings
