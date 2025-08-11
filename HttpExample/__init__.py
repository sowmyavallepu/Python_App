import azure.functions as func
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

# Adjust this import if your FastAPI app is defined elsewhere
from app.main import app as fastapi_app

main = func.WsgiMiddleware(fastapi_app)
