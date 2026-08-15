from fastapi import FastAPI
from api.tasks import router as tasks_router


app = FastAPI(
    title="FastAPI Learning Lab",
    description="A learning project for building production-minded REST APIs.",
    version ="0.1.0",
)

app.include_router(tasks_router)


@app.get("/health", tags=["Health"])
def health_check() -> dict[str, str]:
    """Return the API health status"""
    return {"status": "ok"}