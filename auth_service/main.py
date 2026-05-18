from fastapi import FastAPI

from app.api.auth_router import router as auth_router


app = FastAPI(
    title="Auth Service",
    version="1.0.0",
)


@app.get("/")
async def root():
    return {"status": "ok"}


app.include_router(auth_router)