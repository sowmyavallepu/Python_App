from fastapi import FastAPI
import logging
from app.api import router as api_router  # Import the router

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="FastAPI Azure Function",
    description="A FastAPI application running on Azure Functions",
    version="1.0.0"
)

# Include the API router under the /api prefix
app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    a = 10
    b = 5
    print(a <> b)
    logger.info(f"Comparing {a} != {b}: {a != b}")  # Use logging instead of print
    return {"message": "Hello World from FastAPI on Azure!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    logger.info(f"Fetching item with ID: {item_id}")
    return {"item_id": item_id}

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "FastAPI"}
