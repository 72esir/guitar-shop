from fastapi import FastAPI

from app.api.auth_router import router as auth_router

from prometheus_fastapi_instrumentator import Instrumentator


app = FastAPI(
    title="Auth Service",
    version="1.0.0",
    docs_url="/auth/docs",
    openapi_url="/auth/openapi.json"
)

Instrumentator().instrument(app).expose(app)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(auth_router)