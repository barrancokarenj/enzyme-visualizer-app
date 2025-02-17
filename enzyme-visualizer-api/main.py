from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import visualization
from utils.datahandler import load_parent_sequence, load_variants_data

# Initialize FastAPI with metadata.
app = FastAPI(title="Enzyme Visualization API", version="1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,  # Allow credentials
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(visualization.router)

@app.on_event("startup")
def startup_event():
    """
    Load the parent sequence and variants data when the API starts.

    Raises:
        HTTPException: If there is an error during startup.
    """
    try:

        app.state.parent_sequence = load_parent_sequence()
        app.state.variants_data = load_variants_data()
        # Sort variants by mutation position.
        app.state.variants_data.sort(key=lambda v: v.position)
    except Exception as e:
        logger.error("Startup failed", exc_info=True)
        raise e