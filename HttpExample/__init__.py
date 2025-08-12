import azure.functions as func
import logging
import json

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Get method and basic info
        method = req.method
        url = req.url
        
        # Create response data
        response_data = {
            "message": "Hello from Azure Functions!",
            "method": method,
            "url": url,
            "status": "success"
        }
        
        return func.HttpResponse(
            json.dumps(response_data),
            mimetype="application/json",
            status_code=200
        )
        
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        error_data = {
            "error": str(e),
            "status": "failed"
        }
        return func.HttpResponse(
            json.dumps(error_data),
            mimetype="application/json",
            status_code=500
        )
