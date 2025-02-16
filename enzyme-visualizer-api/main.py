from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from models import Variant
from routers import visualization
import logging

# Initialize FastAPI with metadata.
app = FastAPI(title="Enzyme Visualization API", version="1.0")
app.include_router(visualization.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)
