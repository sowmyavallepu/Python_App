from fastapi import FastAPI
from app.api import router as api_router  # Import the router

app = FastAPI()

# Include the API router under the /api prefix
app.include_router(api_router, prefix="/api")

@app.get("/")
async def read_root():
    return {"message": "Hello World from FastAPI on Azure!"}

@app.get("/items/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}
