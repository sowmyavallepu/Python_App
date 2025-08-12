# tests/test_main_complete.py
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
import sys
import io
from app.main import app

client = TestClient(app)

def test_read_root():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World from FastAPI on Azure!"}

def test_read_root_prints_comparison(capsys):
    """Test that the root endpoint prints the comparison"""
    response = client.get("/")
    captured = capsys.readouterr()
    # The print statement should output True (since 10 != 5)
    assert "True" in captured.out

def test_read_item_positive():
    """Test items endpoint with positive integer"""
    response = client.get("/items/42")
    assert response.status_code == 200
    assert response.json() == {"item_id": 42}

def test_read_item_zero():
    """Test items endpoint with zero"""
    response = client.get("/items/0")
    assert response.status_code == 200
    assert response.json() == {"item_id": 0}

def test_read_item_negative():
    """Test items endpoint with negative integer"""
    response = client.get("/items/-1")
    assert response.status_code == 200
    assert response.json() == {"item_id": -1}

def test_read_item_large_number():
    """Test items endpoint with large number"""
    response = client.get("/items/999999")
    assert response.status_code == 200
    assert response.json() == {"item_id": 999999}

def test_read_item_invalid_string():
    """Test items endpoint with invalid string"""
    response = client.get("/items/invalid")
    assert response.status_code == 422

def test_read_item_float():
    """Test items endpoint with float (should fail validation)"""
    response = client.get("/items/3.14")
    assert response.status_code == 422

def test_api_router_included():
    """Test that API router is properly included"""
    # Test that the app has the API router
    # This will depend on what endpoints your api_router actually has
    # You might need to adjust this based on your actual API routes
    
    # For now, let's test that the router is included by checking app routes
    routes = [route.path for route in app.routes]
    # The API routes should be prefixed with /api
    api_routes = [route for route in routes if route.start
