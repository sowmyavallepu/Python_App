"""
Updated comprehensive test suite for minimal duplicates version
Replace your tests/test_comprehensive.py with this content
"""

import pytest
import sys
import os

# Add the parent directory to sys.path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.duplicates import (
    UserService,
    validate_email, check_email_format,
    validate_password,
    DataProcessor,
    format_api_response
)
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


class TestUserService:
    """Test UserService class"""
    
    def setup_method(self):
        self.user_service = UserService()
    
    def test_create_user_success(self):
        result = self.user_service.create_user("John Doe", "john@example.com", 25)
        assert result["name"] == "John Doe"
        assert result["email"] == "john@example.com"
        assert result["age"] == 25
        assert result["active"] is True
        assert "id" in result
        assert "created_at" in result
        assert "profile" in result
        assert result["profile"]["preferences"]["theme"] == "light"
    
    def test_create_user_invalid_name(self):
        with pytest.raises(ValueError, match="Name must be at least 2 characters"):
            self.user_service.create_user("A", "john@example.com", 25)
        with pytest.raises(ValueError):
            self.user_service.create_user("", "john@example.com", 25)
        with pytest.raises(ValueError):
            self.user_service.create_user(None, "john@example.com", 25)
    
    def test_create_user_invalid_email(self):
        with pytest.raises(ValueError, match="Invalid email format"):
            self.user_service.create_user("John", "invalid", 25)
        with pytest.raises(ValueError):
            self.user_service.create_user("John", "", 25)
        with pytest.raises(ValueError):
            self.user_service.create_user("John", None, 25)
    
    def test_create_user_invalid_age(self):
        with pytest.raises(ValueError, match="Invalid age"):
            self.user_service.create_user("John", "john@example.com", -1)
        with pytest.raises(ValueError):
            self.user_service.create_user("John", "john@example.com", 151)
    
    def test_create_user_boundary_values(self):
        # Test boundary ages
        result = self.user_service.create_user("Test", "test@example.com", 0)
        assert result["age"] == 0
        
        result = self.user_service.create_user("Test", "test@example.com", 150)
        assert result["age"] == 150
        
        # Test minimum name length
        result = self.user_service.create_user("AB", "test@example.com", 25)
        assert result["name"] == "AB"
    
    def test_generate_id(self):
        id1 = self.user_service.generate_id()
        id2 = self.user_service.generate_id()
        assert isinstance(id1, str)
        assert isinstance(id2, str)
        assert id1 != id2
        assert len(id1) > 30  # UUID should be long


class TestEmailValidation:
    """Test email validation functions"""
    
    def test_validate_email_valid(self):
        valid_emails = [
            "test@example.com",
            "user.name@domain.co.uk", 
            "test123@test-domain.com",
            "valid@email.net"
        ]
        for email in valid_emails:
            assert validate_email(email) is True
    
    def test_check_email_format_valid(self):
        valid_emails = [
            "simple@example.com",
            "test@domain.org"
        ]
        for email in valid_emails:
            assert check_email_format(email) is True
    
    def test_validate_email_invalid(self):
        invalid_emails = [
            "", None, "invalid", "@example.com", "test@",
            "test..test@example.com", "test@example", 123,
            "test@example..com", "test@.example.com"
        ]
        for email in invalid_emails:
            assert validate_email(email) is False
    
    def test_check_email_format_invalid(self):
        invalid_emails = [
            "", None, "invalid", "@example.com", "test@", 123
        ]
        for email in invalid_emails:
            assert check_email_format(email) is False
    
    def test_email_edge_cases(self):
        # Test case sensitivity
        assert validate_email("Test@Example.COM") is True
        assert check_email_format("TEST@DOMAIN.ORG") is True
        
        # Test long valid email
        long_email = "a" * 60 + "@example.com"
        assert validate_email(long_email) is True
        
        # Test length limits
        too_long_local = "a" * 65 + "@example.com"
        assert validate_email(too_long_local) is False


class TestPasswordValidation:
    """Test password validation function"""
    
    def test_validate_password_strong(self):
        strong_passwords = [
            "StrongPass123!",
            "MySecure$Password2023",
            "Complex&Pass123"
        ]
        for password in strong_passwords:
            result = validate_password(password)
            assert result["valid"] is True
            assert result["strength"] in ["strong", "medium"]
    
    def test_validate_password_weak(self):
        weak_passwords = [
            "weak",
            "12345678", 
            "password",
            "PASSWORD",
            "Pass123"  # Missing special character
        ]
        for password in weak_passwords:
            result = validate_password(password)
            if password:
                assert result["strength"] in ["weak", "medium"]
                assert len(result["errors"]) > 0
    
    def test_password_empty(self):
        result = validate_password("")
        assert result["valid"] is False
        assert "Password is required" in result["errors"]
        
        result = validate_password(None)
        assert result["valid"] is False
        assert "Password is required" in result["errors"]
    
    def test_password_requirements(self):
        # Test individual requirements
        test_cases = [
            ("lowercase123!", ["uppercase"]),
            ("UPPERCASE123!", ["lowercase"]),
            ("UpperLower!", ["digit"]),
            ("UpperLower123", ["special"]),
            ("Short1!", ["8 characters"]),
        ]
        
        for password, expected_errors in test_cases:
            result = validate_password(password)
            for expected_error in expected_errors:
                error_text = " ".join(result["errors"])
                assert expected_error in error_text
    
    def test_password_suggestions(self):
        medium_password = "Pass123!"  # 8 chars, should get suggestion
        result = validate_password(medium_password)
        if len(medium_password) < 12 and result["valid"]:
            suggestion_text = " ".join(result["suggestions"])
            assert "12 characters" in suggestion_text


class TestDataProcessor:
    """Test DataProcessor class"""
    
    def setup_method(self):
        self.processor = DataProcessor()
    
    def test_process_data_success(self):
        test_data = [{
            "id": "1",
            "name": "Test Item",
            "description": "This is a test",
            "category": "TEST",
            "tags": ["tag1", "tag2"]
        }]
        
        result = self.processor.process_data(test_data)
        assert len(result) == 1
        assert result[0]["id"] == "1"
        assert result[0]["name"] == "Test Item"
        assert result[0]["category"] == "test"
        assert result[0]["tags"] == ["tag1", "tag2"]
        assert "metadata" in result[0]
    
    def test_process_data_empty(self):
        assert self.processor.process_data([]) == []
        assert self.processor.process_data(None) == []
    
    def test_process_data_invalid_items(self):
        invalid_data = [
            "not a dict",
            {"id": "1"},  # Missing name
            {"name": "test"},  # Missing id
            {"id": "2", "name": "valid item"}
        ]
        result = self.processor.process_data(invalid_data)
        assert len(result) == 1
        assert result[0]["name"] == "Valid Item"
    
    def test_process_data_word_count(self):
        test_cases = [
            ({"id": "1", "name": "test", "description": ""}, 0),
            ({"id": "1", "name": "test", "description": "one"}, 1),
            ({"id": "1", "name": "test", "description": "one two three"}, 3),
        ]
        
        for test_item, expected_count in test_cases:
            result = self.processor.process_data([test_item])
            assert result[0]["word_count"] == expected_count
    
    def test_process_data_string_processing(self):
        test_data = [{
            "id": "  123  ",
            "name": "  test item  ",
            "description": "  description  ",
            "category": "UPPERCASE",
            "tags": ["  TAG1  ", "tag2"]
        }]
        
        result = self.processor.process_data(test_data)
        assert result[0]["id"] == "123"
        assert result[0]["name"] == "Test Item"
        assert result[0]["category"] == "uppercase"
        assert result[0]["tags"] == ["tag1", "tag2"]


class TestAPIResponseFormatting:
    """Test API response formatting"""
    
    def test_format_api_response_success(self):
        test_data = {"key": "value"}
        result = format_api_response(test_data)
        
        assert result["success"] is True
        assert result["status_code"] == 200
        assert result["data"] == test_data
        assert "timestamp" in result
        assert "metadata" in result
    
    def test_format_api_response_error(self):
        result = format_api_response({}, "Error", 400)
        assert result["success"] is False
        assert result["status_code"] == 400
        assert "error" in result
        assert result["error"]["code"] == 400
    
    def test_format_api_response_list_data(self):
        list_data = [{"id": 1}, {"id": 2}]
        result = format_api_response(list_data)
        assert result["metadata"]["count"] == 2
        assert result["metadata"]["has_more"] is False
        assert result["metadata"]["page"] == 1
    
    def test_format_api_response_different_status_codes(self):
        test_cases = [
            (200, True), (201, True), (400, False), (404, False), (500, False)
        ]
        for status_code, expected_success in test_cases:
            result = format_api_response({}, "Test", status_code)
            assert result["success"] == expected_success
            assert result["status_code"] == status_code


class TestMainApp:
    """Test main FastAPI application"""
    
    def test_root_endpoint(self):
        response = client.get("/")
        assert response.status_code == 200
        json_data = response.json()
        assert "message" in json_data
    
    def test_api_endpoint(self):
        response = client.get("/api/")
        assert response.status_code == 200
    
    def test_items_endpoint(self):
        response = client.get("/items/123")
        assert response.status_code == 200
        json_data = response.json()
        assert json_data["item_id"] == 123
    
    def test_openapi_schema(self):
        response = client.get("/openapi.json")
        assert response.status_code == 200
        schema = response.json()
        assert "openapi" in schema
    
    def test_docs_endpoint(self):
        response = client.get("/docs")
        assert response.status_code == 200
    
    def test_nonexistent_endpoint(self):
        response = client.get("/nonexistent")
        assert response.status_code == 404


class TestImportsAndModules:
    """Test imports work correctly"""
    
    def test_all_imports_work(self):
        from app.main import app
        assert app is not None
        
        from app.duplicates import (
            UserService, validate_email, validate_password, 
            DataProcessor, format_api_response
        )
        
        assert UserService is not None
        assert validate_email is not None
        assert validate_password is not None
        assert DataProcessor is not None
        assert format_api_response is not None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--cov=app", "--cov-report=term-missing"])
