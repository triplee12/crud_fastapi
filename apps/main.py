#!/usr/bin/python3
"""CRUD API using fastapi and postgresql"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from models.base_models import PostModel, UserModel,VoteModel
# from schemas.database import engine
from crud_fastapi.routes import (
    posts as posts_routes,
    users as users_routes,
    auth,
    votes as likes_routes
)

# users.Base.metadata.create_all(bind=engine)
# posts.Base.metadata.create_all(bind=engine)
# votes.Base.metadata.create_all(bind=engine)

origins = [
    "*",
]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth.router)
app.include_router(posts_routes.route)
app.include_router(users_routes.route)
app.include_router(likes_routes.router)


@app.get("/")
async def root():
    """Root route"""
    return {"message": "Welcome to my API world!"}
