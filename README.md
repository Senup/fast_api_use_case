# FastAPI Learning Lab

A hands-on project for designing, building, testing, and documenting production-minded REST APIs with FastAPI. The domain is intentionally kept simple—a **Task Management API**—so that all complexity comes from the framework, API design, and engineering practices rather than from business rules.

---

## Current status

> **Active development — preparing the FastAPI foundation.**

The repository is being set up. The project direction and roadmap are defined; implementation begins with Milestone 1.

---

## Goals

This project is a deliberate learning curriculum covering:

- **REST API design** — resource modelling, HTTP methods, status codes, and URL conventions
- **FastAPI and Pydantic** — routing, request/response models, dependency injection, and OpenAPI docs
- **Validation and contracts** — input validation, error responses, and schema evolution
- **Application architecture** — routers, service layers, configuration, and project structure
- **PostgreSQL, SQLAlchemy, and Alembic** — async persistence, migrations, pagination, and filtering
- **Authentication and authorisation** — OAuth2/JWT, roles, and service/API keys
- **Testing** — pytest and httpx for unit and integration tests with dependency overrides
- **Docker** — containerised development with Docker Compose
- **Code quality and CI** — Ruff, type checking, and GitHub Actions
- **Documentation** — learning-journal README, OpenAPI docs, and inline docstrings

---

## Application

### Task fields

| Field | Type | Notes |
|---|---|---|
| `id` | UUID | Auto-generated |
| `title` | string | Required |
| `description` | string | Optional |
| `status` | enum | `todo`, `in_progress`, `done` |
| `priority` | enum | `low`, `medium`, `high` |
| `due_date` | date | Optional |
| `created_at` | datetime | Auto-set on creation |
| `updated_at` | datetime | Auto-updated on change |

---

## Planned stack

| Technology | Role |
|---|---|
| **FastAPI** | Web framework |
| **Python 3.11+** | Language |
| **Pydantic v2** | Data validation and serialisation |
| **uv** | Dependency and environment management |
| **PostgreSQL** | Relational database |
| **SQLAlchemy 2.x** | ORM and async database access |
| **Alembic** | Database migrations |
| **pytest / httpx** | Testing |
| **Ruff / type checking** | Linting, formatting, and static analysis |
| **Docker / Docker Compose** | Containerised local development |
| **GitHub Actions** | Continuous integration |

---

## Roadmap

### Milestone 1 — FastAPI foundation
- [ ] Initialise project with `uv`
- [ ] First FastAPI application
- [ ] `GET /health` endpoint
- [ ] Automatic OpenAPI docs at `/docs` and `/redoc`
- [ ] Basic project structure (app, routers, schemas)
- [ ] `.env.example` and `.gitignore`

### Milestone 2 — REST CRUD and validation
- [ ] `POST /api/v1/tasks` — create a task
- [ ] `GET /api/v1/tasks` — list tasks with query parameters
- [ ] `GET /api/v1/tasks/{id}` — retrieve a task
- [ ] `PATCH /api/v1/tasks/{id}` — update a task
- [ ] `DELETE /api/v1/tasks/{id}` — delete a task
- [ ] Pydantic validation and consistent error responses
- [ ] Response models with correct status codes
- [ ] In-memory persistence

### Milestone 3 — Application architecture
- [ ] Routers and versioned API prefix (`/api/v1`)
- [ ] Schemas module (request vs response models)
- [ ] Service layer
- [ ] Dependency injection with `Depends`
- [ ] Configuration via environment variables
- [ ] Centralised exception handlers and logging

### Milestone 4 — Database and migrations
- [ ] Docker Compose with PostgreSQL
- [ ] SQLAlchemy 2.x models and async sessions
- [ ] Alembic migration workflow
- [ ] Pagination, filtering, and sorting on task list
- [ ] Repository pattern for data access

### Milestone 5 — Authentication and authorisation
- [ ] User registration and login endpoints
- [ ] Password hashing
- [ ] OAuth2 password flow with JWT access tokens
- [ ] Protected task routes
- [ ] Role-based access: `admin` and `user`
- [ ] Service/API keys (advanced)

### Milestone 6 — Quality, security, and delivery
- [ ] pytest and httpx integration tests
- [ ] Test database and dependency overrides
- [ ] Ruff linting and formatting
- [ ] Type checking (mypy or Pyright)
- [ ] GitHub Actions CI pipeline
- [ ] CORS, rate limiting, and secure configuration
- [ ] OWASP API Security Top 10 review
- [ ] Docker image for the application
- [ ] README portfolio polish, changelog, and release tags

---

## Planned endpoints

| Method | Path | Description |
|---|---|---|
| `GET` | `/health` | Health check |
| `GET` | `/api/v1/tasks` | List tasks |
| `POST` | `/api/v1/tasks` | Create a task |
| `GET` | `/api/v1/tasks/{id}` | Get a task |
| `PATCH` | `/api/v1/tasks/{id}` | Update a task |
| `DELETE` | `/api/v1/tasks/{id}` | Delete a task |
| `POST` | `/api/v1/auth/register` | Register a user |
| `POST` | `/api/v1/auth/token` | Obtain a JWT access token |

---

## Local setup

> Setup instructions will expand as the application is implemented. The steps below cover prerequisites and cloning the repository.

### Prerequisites

- Ubuntu Linux
- Python 3.11+
- Git
- VS Code (recommended)

### Install uv

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Verify the installation:

```bash
uv --version
```

### Clone the repository

```bash
git clone https://github.com/wibnudixon/rest_api_use_case.git
cd rest_api_use_case
```

---

## Learning journal

### Milestone 0 — Project direction

**Key decisions and reasoning:**

- **Learning lab, not a domain-heavy app.** The focus is on mastering FastAPI concepts—routing, validation, dependency injection, testing, authentication, and deployment—rather than on building complex business logic. Keeping the domain simple means all difficulty comes from the framework and engineering practices.

- **Task Management API as the vehicle.** Tasks are familiar and small enough to stay out of the way, while still providing realistic fields (`status`, `priority`, `due_date`) that exercise Pydantic enums, optional fields, and datetime handling.

- **`uv` for dependency management.** `uv` is significantly faster than traditional `pip` + `venv` and produces a lockfile for reproducible installs. It is also the modern standard in the Python ecosystem. The relevant commands (`uv init`, `uv add`, `uv run`, `uv sync`) will be introduced only when needed.

- **One evolving application.** Rather than isolated experiment folders, a single growing API is more representative of real-world development. Git history and README milestones document the learning progression.

- **REST-only first.** REST fundamentals must be solid before exploring GraphQL, gRPC, event-driven patterns, or cloud integrations. Staying REST-only keeps the learning path focused and the API surface predictable.

**Next up**

- [ ] Initialise the project with `uv init`
- [ ] Create the first FastAPI application
- [ ] Implement `GET /health`
- [ ] Explore the auto-generated `/docs`

---

## Repository principles

- **Learn by building.** Every concept is introduced through working code, not theory alone.
- **Start simple.** Begin with the smallest thing that works; add complexity only when the foundation is solid.
- **Prefer clarity over cleverness.** Code in this repository should be easy to read and understand.
- **Treat it as public from day one.** No secrets, no hard-coded credentials, no throwaway shortcuts.
- **Build incrementally.** Each milestone produces a complete, runnable application—not a work-in-progress skeleton.

---

## License

This is a learning and portfolio project. An **MIT License** will be added before the repository is made public.

---

## Author

**wibnudixon** — [github.com/wibnudixon](https://github.com/wibnudixon)

If you are also learning FastAPI, feel free to explore the repository, follow along with the milestones, or open an issue to share ideas. Everyone starts somewhere—welcome.
