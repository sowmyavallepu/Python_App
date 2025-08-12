import azure.functions as func
import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(title="Azure Function FastAPI", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {"message": "Hello from Azure Functions + FastAPI!"}

@app.get("/api/test")
async def test():
    return {"message": "Test endpoint working", "status": "success"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Azure Functions entry point
def main(req: func.HttpRequest) -> func.HttpResponse:
    try:
        logger.info('Python HTTP trigger function processed a request.')
        
        # Import here to avoid issues
        from fastapi import FastAPI
        from fastapi.responses import JSONResponse
        import asyncio
        
        # Handle the request
        path = req.route_params.get('path', '')
        method = req.method.lower()
        
        logger.info(f'Request: {method} {path}')
        
        # Simple routing for now
        if method == 'get':
            if path == '' or path == '/':
                return func.HttpResponse(
                    '{"message": "Hello from Azure Functions + FastAPI!"}',
                    mimetype="application/json",
                    status_code=200
                )
            elif path == 'test' or path == '/test':
                return func.HttpResponse(
                    '{"message": "Test endpoint working", "status": "success"}',
                    mimetype="application/json",
                    status_code=200
                )
            elif path == 'health' or path == '/health':
                return func.HttpResponse(
                    '{"status": "healthy"}',
                    mimetype="application/json",
                    status_code=200
                )
        
        # Default response
        return func.HttpResponse(
            '{"message": "Azure Function is working"}',
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logger.error(f'Error processing request: {str(e)}')
        return func.HttpResponse(
            f'{{"error": "Internal server error", "details": "{str(e)}"}}',
            mimetype="application/json",
            status_code=500
        )
