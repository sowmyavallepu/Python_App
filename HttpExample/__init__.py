import azure.functions as func
import logging
from fastapi import FastAPI
from fastapi.responses import JSONResponse
import asyncio
import json
from typing import Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Azure Function FastAPI", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "Hello from Azure Functions + FastAPI!", "status": "success"}

@app.get("/test")
async def test():
    return {"message": "Test endpoint working", "status": "success"}

@app.get("/api/test")
async def api_test():
    return {"message": "API Test endpoint working", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "FastAPI on Azure Functions"}

@app.post("/")
async def post_root(data: Dict[Any, Any] = None):
    return {"message": "POST request received", "data": data, "status": "success"}

# Convert Azure Function request to FastAPI format
def convert_azure_request_to_fastapi(req: func.HttpRequest, path: str):
    """Convert Azure Function HTTP request to format FastAPI can handle"""
    
    # Build the scope dict that ASGI expects
    scope = {
        "type": "http",
        "method": req.method,
        "path": f"/{path}" if path and not path.startswith('/') else path or "/",
        "query_string": req.url.split('?', 1)[1].encode() if '?' in req.url else b"",
        "headers": [(k.lower().encode(), v.encode()) for k, v in req.headers.items()],
    }
    
    return scope

# Azure Functions entry point
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logger.info(f'Processing {req.method} request')
        
        # Get the path from route params
        path = req.route_params.get('path', '').strip('/')
        
        logger.info(f'Request path: {path}')
        logger.info(f'Request method: {req.method}')
        
        # Handle different endpoints manually for now (simpler than full ASGI)
        if req.method == 'GET':
            if path == '' or path == '/':
                result = {"message": "Hello from Azure Functions + FastAPI!", "status": "success"}
            elif path == 'test':
                result = {"message": "Test endpoint working", "status": "success"}
            elif path == 'api/test':
                result = {"message": "API Test endpoint working", "status": "success"}
            elif path == 'health':
                result = {"status": "healthy", "service": "FastAPI on Azure Functions"}
            else:
                result = {
                    "error": f"Endpoint GET /{path} not found",
                    "available_endpoints": ["/", "/test", "/api/test", "/health"]
                }
                return func.HttpResponse(
                    json.dumps(result),
                    mimetype="application/json",
                    status_code=404
                )
        elif req.method == 'POST':
            try:
                request_data = req.get_json() if req.get_body() else {}
                result = {"message": "POST request received", "data": request_data, "status": "success"}
            except Exception as e:
                result = {"error": "Invalid JSON", "details": str(e)}
                return func.HttpResponse(
                    json.dumps(result),
                    mimetype="application/json",
                    status_code=400
                )
        else:
            result = {"error": f"Method {req.method} not allowed"}
            return func.HttpResponse(
                json.dumps(result),
                mimetype="application/json",
                status_code=405
            )
        
        return func.HttpResponse(
            json.dumps(result),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f'Error processing request: {str(e)}', exc_info=True)
        error_response = {
            "error": "Internal server error",
            "message": str(e),
            "type": type(e).__name__
        }
        return func.HttpResponse(
            json.dumps(error_response),
            mimetype="application/json",
            status_code=500
        )
