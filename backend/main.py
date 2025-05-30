from db.base import Base
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes.auth import auth_router
from db.db import engine

app = FastAPI()

origins = ["https://localhost", "http://localhost:3000"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(auth_router,prefix="/auth")

@app.get("/")
def root():
    return "Fastb api up and running"

Base.metadata.create_all(engine)