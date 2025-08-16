# Add this code to the END of your tests/test_comprehensive.py file

class TestCoverageBooster:
    """Additional comprehensive tests to push coverage above 95%"""
    
    def test_user_service_all_edge_cases(self):
        """Test every edge case in UserService"""
        user_service = UserService()
        
        # Test with minimal data
        user = user_service.create_user("A", "a@b.co", 18)
        assert user["name"] == "A"
        assert user["age"] == 18
        
        # Test with maximum length data
        long_name = "A" * 100
        user = user_service.create_user(long_name, "long@example.com", 99)
        assert user["name"] == long_name
        
        # Test ID generation multiple times to hit all code paths
        ids = []
        for i in range(5):
            uid = user_service.generate_id()
            assert len(uid) > 20
            ids.append(uid)
        
        # Ensure all IDs are unique
        assert len(set(ids)) == 5
        
        # Test profile structure completely
        assert "profile" in user
        assert "bio" in user["profile"]
        assert "avatar" in user["profile"]
        assert "preferences" in user["profile"]
        assert "notifications" in user["profile"]["preferences"]
    
    def test_data_processor_complete_paths(self):
        """Test all code paths in DataProcessor"""
        processor = DataProcessor()
        
        # Test empty list
        result = processor.process_data([])
        assert result == []
        
        # Test single item
        single_item = [{"id": "1", "name": "Test", "description": "A test item"}]
        result = processor.process_data(single_item)
        assert len(result) == 1
        assert result[0]["word_count"] == 3
        
        # Test multiple items with various whitespace scenarios
        complex_data = [
            {"id": "\n\t 123 \r\n", "name": "  Item One  ", "description": "First test item here"},
            {"id": "456", "name": "Item\tTwo", "description": "Second item description"},
            {"id": " 789 ", "name": "\r\nItem Three\n", "description": "Third and final item"}
        ]
        
        result = processor.process_data(complex_data)
        assert len(result) == 3
        
        # Verify each item was processed correctly
        assert result[0]["id"] == "123"
        assert result[0]["name"] == "Item One"
        assert result[0]["word_count"] == 4
        
        assert result[1]["name"] == "Item Two"
        assert result[1]["word_count"] == 3
        
        assert result[2]["name"] == "Item Three"
        assert result[2]["word_count"] == 4
        
        # Test metadata in all items
        for item in result:
            assert "metadata" in item
            assert item["metadata"]["version"] == "1.0"
            assert item["metadata"]["status"] == "active"
            assert "processed_at" in item["metadata"]
    
    def test_validation_functions_comprehensive(self):
        """Test all validation scenarios thoroughly"""
        
        # Test validate_email with edge cases
        edge_cases = [
            ("user@domain.com", True),
            ("user.name@domain.com", True),
            ("user+tag@domain.com", True),
            ("user@sub.domain.com", True),
            ("", False),
            ("invalid", False),
            ("@domain.com", False),
            ("user@", False),
            ("user@@domain.com", False),
            ("user@domain", False)  # No TLD
        ]
        
        for email, expected in edge_cases:
            assert validate_email(email) == expected, f"Failed for email: {email}"
        
        # Test check_email_format separately
        assert check_email_format("test@example.org") is True
        assert check_email_format("bad-email") is False
        
        # Test validate_password with all scenarios
        password_tests = [
            ("password123", True),  # Valid
            ("pass", False),        # Too short
            ("", False),           # Empty
            ("a" * 100, True),     # Long but valid
            ("P@ssw0rd!", True),   # Complex valid
            ("123", False)         # Too short
        ]
        
        for password, expected in password_tests:
            assert validate_password(password) == expected, f"Failed for password: {password}"
    
    def test_api_response_all_data_types(self):
        """Test format_api_response with every data type"""
        
        test_cases = [
            # Basic types
            ("string", str),
            (123, int),
            (45.67, float),
            (True, bool),
            (False, bool),
            
            # Complex types
            ({"key": "value"}, dict),
            ([1, 2, 3], list),
            (None, type(None)),
            
            # Empty collections
            ({}, dict),
            ([], list),
            ("", str)
        ]
        
        for data, data_type in test_cases:
            result = format_api_response(data)
            
            # Verify structure
            assert "success" in result
            assert "data" in result
            assert "timestamp" in result
            assert "metadata" in result
            
            # Verify data
            assert result["success"] is True
            if data is not None:
                assert isinstance(result["data"], data_type)
            else:
                assert result["data"] is None
            
            # Verify metadata structure
            metadata = result["metadata"]
            assert "request_id" in metadata
            assert "version" in metadata
            assert "api_version" in metadata
            assert metadata["version"] == "1.0"
            assert metadata["api_version"] == "v1"
            
            # Verify timestamp format
            assert isinstance(result["timestamp"], str)
            assert len(result["timestamp"]) > 10  # ISO format
    
    def test_error_handling_and_edge_cases(self):
        """Test error handling and extreme edge cases"""
        
        # Test UserService with edge case ages
        user_service = UserService()
        
        young_user = user_service.create_user("Young", "young@test.com", 1)
        assert young_user["age"] == 1
        
        old_user = user_service.create_user("Old", "old@test.com", 120)
        assert old_user["age"] == 120
        
        # Test DataProcessor with edge case data
        processor = DataProcessor()
        
        # Test with items that have minimal descriptions
        minimal_data = [
            {"id": "1", "name": "A", "description": "B"},
            {"id": "2", "name": "X", "description": "Y Z"}
        ]
        
        result = processor.process_data(minimal_data)
        assert result[0]["word_count"] == 1  # "B"
        assert result[1]["word_count"] == 2  # "Y Z"
        
        # Test with whitespace-only descriptions
        whitespace_data = [
            {"id": "3", "name": "Test", "description": "   "},
            {"id": "4", "name": "Test2", "description": "\n\t\r"}
        ]
        
        result = processor.process_data(whitespace_data)
        for item in result:
            assert item["word_count"] == 0  # Should be 0 for whitespace-only
    
    def test_all_imports_and_modules(self):
        """Test that all imports work and are accessible"""
        
        # Test datetime functionality
        from app.duplicates import datetime
        now = datetime.datetime.now()
        assert hasattr(now, 'isoformat')
        iso_string = now.isoformat()
        assert isinstance(iso_string, str)
        assert 'T' in iso_string  # ISO format has T
        
        # Test json functionality  
        from app.duplicates import json
        test_dict = {"test": "value", "number": 42}
        json_str = json.dumps(test_dict)
        assert isinstance(json_str, str)
        parsed = json.loads(json_str)
        assert parsed == test_dict
        
        # Test typing imports
        from app.duplicates import Dict, List, Optional, Any
        
        # These should not raise import errors
        assert Dict is not None
        assert List is not None  
        assert Optional is not None
        assert Any is not None
        
        # Test uuid functionality (used in generate_id)
        import uuid
        test_uuid = str(uuid.uuid4())
        assert len(test_uuid) == 36  # Standard UUID length
        assert test_uuid.count('-') == 4  # UUID format
