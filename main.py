from fastapi import FastAPI
from contextlib import asynccontextmanager
# ABSOLUTE IMPORTS (No leading dots)
from database import create_db_and_tables
from controllers import user_controller

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield

app = FastAPI(
    title="Hutang Bayarlah API",
    lifespan=lifespan
)

app.include_router(user_controller.router)

@app.get("/")
def root():
    return {"status": "Backend is running!"}