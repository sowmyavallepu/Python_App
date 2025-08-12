import azure.functions as func
import logging

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    try:
        # Simple response without any complex logic
        return func.HttpResponse(
            "Hello, World! This Azure Function is working.",
            status_code=200
        )
    except Exception as e:
        logging.error(f'Error: {str(e)}')
        return func.HttpResponse(
            f"Error: {str(e)}",
            status_code=500
        )
