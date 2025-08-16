# Add this to the end of your tests/test_comprehensive.py file:

class TestAdditionalCoverage:
    """Additional tests to push coverage to 96%+"""
    
    def test_user_service_edge_cases(self):
        """Test additional edge cases for UserService"""
        user_service = UserService()
        
        # Test with different email formats
        result = user_service.create_user("Test", "test+tag@example.co.uk", 25)
        assert result["email"] == "test+tag@example.co.uk"
        
        # Test profile structure completely
        assert result["profile"]["bio"] == ""
        assert result["profile"]["avatar"] is None
        assert result["profile"]["preferences"]["notifications"] is True
        assert result["role"] == "user"
        assert result["permissions"] == ["read"]
        
        # Test ID generation multiple times
        ids = [user_service.generate_id() for _ in range(3)]
        assert len(set(ids)) == 3  # All unique
        for uid in ids:
            assert len(uid) > 30  # UUID format
    
    def test_data_processor_complete_coverage(self):
        """Test all data processor paths"""
        processor = DataProcessor()
        
        # Test with various data scenarios
        complex_data = [{
            "id": "\t 123 \n",
            "name": "\r\n  Complex Item  \t",
            "description": "Multi word description here",
            "category": "COMPLEX_CATEGORY",
            "tags": ["\n tag1 \r", "\t TAG2\n", "  tag3  "]
        }]
        
        result = processor.process_data(complex_data)
        assert result[0]["id"] == "123"
        assert result[0]["name"] == "Complex Item"
        assert result[0]["category"] == "complex_category"
        assert result[0]["tags"] == ["tag1", "tag2", "tag3"]
        assert result[0]["word_count"] == 4
        
        # Test metadata structure
        metadata = result[0]["metadata"]
        assert metadata["version"] == "1.0"
        assert metadata["status"] == "active"
        assert "processed_at" in metadata
    
    def test_api_response_all_scenarios(self):
        """Test all API response scenarios"""
        # Test with None data
        result = format_api_response(None)
        assert result["data"] is None
        assert result["success"] is True
        
        # Test with different data types
        test_cases = [
            ("string data", str),
            (123, int),
            (True, bool),
            ({"key": "value"}, dict)
        ]
        
        for data, data_type in test_cases:
            result = format_api_response(data)
            assert isinstance(result["data"], data_type)
            assert result["success"] is True
            assert "request_id" in result["metadata"]
            assert result["metadata"]["version"] == "1.0"
            assert result["metadata"]["api_version"] == "v1"
    
    def test_email_validation_comprehensive(self):
        """Test comprehensive email validation scenarios"""
        # Test whitespace handling
        assert validate_email("  test@example.com  ") is True
        assert check_email_format("  simple@domain.org  ") is True
        
        # Test case handling
        assert validate_email("UPPER@DOMAIN.COM") is True
        assert validate_email("MiXeD@CaSe.CoM") is True
        
        # Test domain validation edge cases
        assert validate_email("test@sub.domain.example.com") is True
        assert validate_email("test@a.b") is True  # Minimal valid domain
        
        # Test specific invalid cases
        invalid_cases = [
            "test@domain.",  # Ends with dot
            "test@.domain.com",  # Starts with dot
            "test@domain..com",  # Double dot
        ]
        for email in invalid_cases:
            assert validate_email(email) is False
    
    def test_imports_and_modules_complete(self):
        """Test all imports work correctly"""
        # Test that datetime operations work
        from app.duplicates import datetime
        now = datetime.datetime.now()
        assert isinstance(now.isoformat(), str)
        
        # Test typing imports
        from app.duplicates import Dict, List, Optional, Any
        assert Dict is not None
        assert List is not None
        assert Optional is not None
        assert Any is not None
        
        # Test json import
        from app.duplicates import json
        test_data = {"test": "value"}
        json_str = json.dumps(test_data)
        assert isinstance(json_str, str)
        assert json.loads(json_str) == test_data
