#!/usr/bin/python3
"""CRUD API using fastapi and postgresql"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from crud_fastapi.models import posts, users
from crud_fastapi.schemas.database import engine
from crud_fastapi.routes import (
    posts as posts_routes,
    users as users_routes,
    auth
)

users.Base.metadata.create_all(bind=engine)
posts.Base.metadata.create_all(bind=engine)

origins = [
    "http://localhost:3000",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(posts_routes.route)
app.include_router(users_routes.route)
app.include_router(auth.router)


@app.get("/")
async def root():
    """Root route"""
    return {"messaga": "Welcome to my API world!"}
