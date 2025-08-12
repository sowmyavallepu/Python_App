# tests/test_main.py
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint - this will cover your read_root function"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from FastAPI on Azure!"}

def test_read_item_valid():
    """Test the items endpoint with valid item_id"""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}

def test_read_item_negative():
    """Test the items endpoint with negative item_id"""
    response = client.get("/items/-1")
    assert response.status_code == 200
    assert response.json() == {"item_id": -1}

def test_read_item_zero():
    """Test the items endpoint with zero item_id"""
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == {"item_id": 0}

def test_read_item_invalid_string():
    """Test the items endpoint with invalid string item_id"""
    response = client.get("/items/invalid")
    assert response.status_code == 422  # Validation error

def test_read_item_float():
    """Test the items endpoint with float item_id"""
    response = client.get("/items/3.14")
    assert response.status_code == 422  # Validation error

# tests/test_api_router.py
def test_api_endpoints():
    """Test API router endpoints (adjust based on your actual API)"""
    # Add tests for your API router endpoints
    # Example:
    # response = client.get("/api/some-endpoint")
    # assert response.status_code == 200
    pass
