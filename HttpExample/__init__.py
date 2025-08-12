import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Create FastAPI app directly here
fastapi_app = FastAPI()

@fastapi_app.get("/")
async def root():
    return {"message": "Hello World"}

@fastapi_app.get("/test")
async def test():
    return {"message": "Test endpoint"}

# Azure Function
main = func.WsgiMiddleware(fastapi_app).handle

# import azure.functions as func
# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware

# # Adjust this import if your FastAPI app is defined elsewhere
# from app.main import app as fastapi_app

# main = func.WsgiMiddleware(fastapi_app)
