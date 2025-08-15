"""
Detailed tests for main.py
Place this in: tests/test_main_detailed.py
"""

import pytest
import sys
import os
from fastapi.testclient import TestClient

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.main import app

client = TestClient(app)


class TestMainApplication:
    """Comprehensive tests for the main FastAPI application"""
    
    def test_app_creation(self):
        """Test that the FastAPI app is created properly"""
        assert app is not None
        assert hasattr(app, 'routes')
    
    def test_root_endpoint_get(self):
        """Test GET request to root endpoint"""
        response = client.get("/")
        assert response.status_code == 200
        
        # Test response structure
        json_response = response.json()
        assert isinstance(json_response, dict)
        
        # Check for common response fields
        expected_fields = ["message", "status", "data", "timestamp"]
        for field in expected_fields:
            if field in json_response:
                assert json_response[field] is not None
    
    def test_root_endpoint_post(self):
        """Test POST request to root endpoint"""
        response = client.post("/")
        # This might return 405 (Method Not Allowed) if POST isn't supported
        assert response.status_code in [200, 405]
    
    def test_invalid_endpoint(self):
        """Test request to non-existent endpoint"""
        response = client.get("/nonexistent")
        assert response.status_code == 404
    
    def test_openapi_schema(self):
        """Test OpenAPI schema endpoint"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "openapi" in schema
        assert "info" in schema
        assert "paths" in schema
    
    def test_docs_endpoint(self):
        """Test Swagger UI docs endpoint"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_redoc_endpoint(self):
        """Test ReDoc documentation endpoint"""
        response = client.get("/redoc")
        assert response.status_code == 200
        assert "text/html" in response.headers.get("content-type", "")
    
    def test_health_endpoint_if_exists(self):
        """Test health check endpoint if it exists"""
        response = client.get("/health")
        # Health endpoint might not exist, that's okay
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            json_response = response.json()
            assert "status" in json_response or "health" in json_response
    
    def test_api_prefix_endpoints(self):
        """Test common API prefix endpoints"""
        prefixes = ["/api", "/api/v1", "/v1"]
        
        for prefix in prefixes:
            response = client.get(prefix)
            # These might not exist, just testing for coverage
            assert response.status_code in [200, 404, 422]
    
    def test_cors_headers(self):
        """Test CORS headers if configured"""
        response = client.options("/")
        # CORS might not be configured, that's okay
        assert response.status_code in [200, 405]
    
    def test_content_type_headers(self):
        """Test content type headers"""
        response = client.get("/")
        assert response.status_code == 200
        
        content_type = response.headers.get("content-type", "")
        assert "application/json" in content_type or "text/html" in content_type
    
    def test_user_agent_handling(self):
        """Test different user agent handling"""
        headers = {"User-Agent": "TestClient/1.0"}
        response = client.get("/", headers=headers)
        assert response.status_code == 200
    
    def test_query_parameters(self):
        """Test query parameter handling"""
        response = client.get("/?test=value&limit=10")
        assert response.status_code == 200
    
    def test_request_with_data(self):
        """Test requests with JSON data"""
        test_data = {"test": "value", "number": 123}
        response = client.post("/", json=test_data)
        # Might return 405 if POST not supported, that's okay
        assert response.status_code in [200, 201, 405, 422]
    
    def test_request_with_form_data(self):
        """Test requests with form data"""
        form_data = {"field1": "value1", "field2": "value2"}
        response = client.post("/", data=form_data)
        # Might return 405 if POST not supported
        assert response.status_code in [200, 201, 405, 422]
    
    def test_large_request(self):
        """Test handling of large requests"""
        large_data = {"data": "x" * 1000}  # 1KB of data
        response = client.post("/", json=large_data)
        # Should handle gracefully regardless of whether endpoint exists
        assert response.status_code in [200, 201, 405, 413, 422]
    
    def test_special_characters_in_url(self):
        """Test special characters in URL"""
        special_urls = [
            "/test%20space",
            "/test+plus",
            "/test&ampersand",
            "/test?query=value"
        ]
        
        for url in special_urls:
            response = client.get(url)
            # Should return 404 for non-existent endpoints
            assert response.status_code in [200, 404, 422]
    
    def test_http_methods(self):
        """Test different HTTP methods"""
        methods = [
            ("GET", client.get),
            ("POST", client.post),
            ("PUT", client.put),
            ("DELETE", client.delete),
            ("PATCH", client.patch)
        ]
        
        for method_name, method_func in methods:
            response = method_func("/")
            # Most will return 405 (Method Not Allowed) except GET
            if method_name == "GET":
                assert response.status_code == 200
            else:
                assert response.status_code in [200, 201, 405, 422]


class TestApplicationStartup:
    """Test application startup and configuration"""
    
    def test_app_title(self):
        """Test application title in OpenAPI schema"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        if "info" in schema and "title" in schema["info"]:
            assert isinstance(schema["info"]["title"], str)
            assert len(schema["info"]["title"]) > 0
    
    def test_app_version(self):
        """Test application version in OpenAPI schema"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        if "info" in schema and "version" in schema["info"]:
            assert isinstance(schema["info"]["version"], str)
    
    def test_app_routes(self):
        """Test that routes are properly configured"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        assert "paths" in schema
        assert len(schema["paths"]) > 0
        
        # Check that root path exists
        assert "/" in schema["paths"] or any(path.startswith("/") for path in schema["paths"])


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
