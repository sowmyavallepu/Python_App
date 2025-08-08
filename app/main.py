from fastapi import FastAPI

app = FastAPI(title="FastAPI Azure App", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello World from FastAPI on Azure!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

# from fastapi import FastAPI
# from app.api import router

# app = FastAPI()
# app.include_router(router)
