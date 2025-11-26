"""FastAPI backend for LLM Council."""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .apis import api_router

app = FastAPI(title="LLM Council API")

# CORS origins - support both local development and production
cors_origins = os.getenv(
    "CORS_ORIGINS",
    "http://localhost:5173,http://localhost:3000"
).split(",")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in cors_origins],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include all API routes
app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
