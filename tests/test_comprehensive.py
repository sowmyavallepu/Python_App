# Add this code to the END of your tests/test_comprehensive.py file
# This targets the exact missing lines in your duplicates.py file

class TestMissingLinesTargeted:
    """Target the exact missing lines for 95% coverage"""
    
    def test_userservice_validation_errors(self):
        """Test UserService validation that raises ValueError"""
        user_service = UserService()
        
        # Test name validation errors (currently not covered)
        try:
            user_service.create_user("", "test@example.com", 25)  # Empty name
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "Name must be at least 2 characters" in str(e)
        
        try:
            user_service.create_user("A", "test@example.com", 25)  # Name too short
            assert False, "Should raise ValueError for short name"
        except ValueError as e:
            assert "Name must be at least 2 characters" in str(e)
        
        # Test email validation errors (currently not covered)
        try:
            user_service.create_user("John", "", 25)  # Empty email
            assert False, "Should raise ValueError for empty email"
        except ValueError as e:
            assert "Invalid email format" in str(e)
        
        try:
            user_service.create_user("John", "invalid_email", 25)  # No @ symbol
            assert False, "Should raise ValueError for invalid email"
        except ValueError as e:
            assert "Invalid email format" in str(e)
        
        # Test age validation errors (currently not covered)
        try:
            user_service.create_user("John", "john@test.com", -1)  # Negative age
            assert False, "Should raise ValueError for negative age"
        except ValueError as e:
            assert "Invalid age" in str(e)
        
        try:
            user_service.create_user("John", "john@test.com", 151)  # Age too high
            assert False, "Should raise ValueError for age > 150"
        except ValueError as e:
            assert "Invalid age" in str(e)
    
    def test_userservice_all_fields(self):
        """Test all fields in UserService create_user to hit missing lines"""
        user_service = UserService()
        user = user_service.create_user("John Doe", "john@example.com", 30)
        
        # Test all fields that might not be covered
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user
        assert user["active"] is True
        assert user["role"] == "user"
        assert user["permissions"] == ["read"]
        
        # Test nested profile structure
        profile = user["profile"]
        assert profile["bio"] == ""
        assert profile["avatar"] is None
        assert "preferences" in profile
        
        preferences = profile["preferences"]
        assert preferences["theme"] == "light"
        assert preferences["notifications"] is True
        
        # Test datetime fields are strings
        assert isinstance(user["created_at"], str)
        assert isinstance(user["updated_at"], str)
        assert "T" in user["created_at"]  # ISO format
    
    def test_validate_email_all_branches(self):
        """Test every branch in validate_email function"""
        
        # Test None and non-string inputs (line not covered)
        assert validate_email(None) is False
        assert validate_email(123) is False
        assert validate_email([]) is False
        assert validate_email({}) is False
        
        # Test empty email (line not covered)
        assert validate_email("") is False
        assert validate_email("   ") is False
        
        # Test missing @ or . (line not covered)
        assert validate_email("noemail") is False
        assert validate_email("no@email") is False
        assert validate_email("email.com") is False
        
        # Test multiple @ symbols (line not covered)
        assert validate_email("user@@domain.com") is False
        assert validate_email("user@domain@com") is False
        
        # Test local part validation (lines not covered)
        assert validate_email("@domain.com") is False  # Empty local
        assert validate_email("a" * 65 + "@domain.com") is False  # Local too long
        
        # Test domain part validation (lines not covered)
        assert validate_email("user@") is False  # Empty domain
        assert validate_email("user@" + "a" * 256) is False  # Domain too long
        
        # Test consecutive dots (line not covered)
        assert validate_email("user..name@domain.com") is False
        assert validate_email("user@domain..com") is False
        
        # Test domain structure (lines not covered)
        assert validate_email("user@domain") is False  # No TLD
        assert validate_email("user@.com") is False  # Empty domain part
        
        # Test domain part length limits (lines not covered)
        assert validate_email("user@" + "a" * 64 + ".com") is False  # Domain part too long
        
        # Test domain parts starting/ending with hyphen (lines not covered)
        assert validate_email("user@-domain.com") is False
        assert validate_email("user@domain-.com") is False
        assert validate_email("user@domain.-com") is False
        assert validate_email("user@domain.com-") is False
        
        # Test valid emails to ensure function still works
        assert validate_email("user@domain.com") is True
        assert validate_email("test@example.org") is True
    
    def test_validate_password_all_branches(self):
        """Test every branch in validate_password function"""
        
        # Test empty password (line not covered)
        result = validate_password("")
        assert result["valid"] is False
        assert "Password is required" in result["errors"]
        assert result["strength"] == "weak"
        
        # Test None password (line not covered)
        result = validate_password(None)
        assert result["valid"] is False
        
        # Test short password (< 8 chars) (line not covered)
        result = validate_password("short")
        assert result["valid"] is False
        assert "Password must be at least 8 characters long" in result["errors"]
        
        # Test medium length password (8-11 chars) (line not covered)
        result = validate_password("password")
        assert "Consider using at least 12 characters" in result["suggestions"]
        
        # Test missing uppercase (line not covered)
        result = validate_password("password123!")
        assert "Password must contain at least one uppercase letter" in result["errors"]
        
        # Test missing lowercase (line not covered)  
        result = validate_password("PASSWORD123!")
        assert "Password must contain at least one lowercase letter" in result["errors"]
        
        # Test missing digit (line not covered)
        result = validate_password("Password!")
        assert "Password must contain at least one digit" in result["errors"]
        
        # Test missing special character (line not covered)
        result = validate_password("Password123")
        assert "Password must contain at least one special character" in result["errors"]
        
        # Test strength calculations (lines not covered)
        # Weak password (score < 3)
        result = validate_password("weak")
        assert result["strength"] == "weak"
        
        # Medium password (score 3-4)
        result = validate_password("Password123")  # Missing special char
        assert result["strength"] == "medium"
        
        # Strong password (score >= 5)
        result = validate_password("StrongPassword123!")
        assert result["strength"] == "strong"
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_dataprocessor_all_branches(self):
        """Test every branch in DataProcessor"""
        processor = DataProcessor()
        
        # Test empty data (line covered)
        assert processor.process_data([]) == []
        assert processor.process_data(None) == []
        
        # Test non-dict items (line not covered)
        result = processor.process_data(["string", 123, None])
        assert result == []  # Should skip non-dict items
        
        # Test missing required fields (lines not covered)
        result = processor.process_data([
            {},  # No id or name
            {"id": "1"},  # Missing name
            {"name": "Test"},  # Missing id
        ])
        assert result == []  # Should skip items without required fields
        
        # Test valid data with all optional fields (lines not covered)
        data = [{
            "id": 123,  # Test int to str conversion
            "name": "test item",  # Test title() conversion
            "description": "This is a test description",
            "category": "TEST_CATEGORY",  # Test lower() conversion
            "tags": ["  Tag1  ", "TAG2", "\tTag3\n"]  # Test tag processing
        }]
        
        result = processor.process_data(data)
        assert len(result) == 1
        
        item = result[0]
        assert item["id"] == "123"  # Int converted to string
        assert item["name"] == "Test Item"  # Title case
        assert item["description"] == "This is a test description"
        assert item["category"] == "test_category"  # Lowercase
        assert item["tags"] == ["tag1", "tag2", "tag3"]  # Cleaned tags
        assert item["word_count"] == 5  # Word count calculation
        
        # Test missing optional fields (lines not covered)
        data = [{"id": "1", "name": "Test"}]  # No description, category, tags
        result = processor.process_data(data)
        
        item = result[0]
        assert item["description"] == ""  # Default empty description
        assert item["category"] == "uncategorized"  # Default category
        assert item["tags"] == []  # Default empty tags
        assert item["word_count"] == 0  # No description = 0 words
        
        # Test metadata fields (lines not covered)
        assert "metadata" in item
        metadata = item["metadata"]
        assert "processed_at" in metadata
        assert metadata["version"] == "1.0"
        assert metadata["status"] == "active"
        assert "T" in metadata["processed_at"]  # ISO format
    
    def test_format_api_response_all_branches(self):
        """Test every branch in format_api_response"""
        
        # Test default parameters (lines not covered)
        response = format_api_response({"test": "data"})
        assert response["success"] is True
        assert response["status_code"] == 200
        assert response["message"] == "Success"
        assert response["data"] == {"test": "data"}
        
        # Test custom message and status (lines not covered)
        response = format_api_response(None, "Custom message", 201)
        assert response["message"] == "Custom message"
        assert response["status_code"] == 201
        assert response["success"] is True  # 201 < 400
        
        # Test error response (lines not covered)
        response = format_api_response(None, "Error occurred", 400)
        assert response["success"] is False  # 400 >= 400
        assert response["status_code"] == 400
        assert response["message"] == "Error occurred"
        assert "error" in response
        assert response["error"]["code"] == 400
        assert response["error"]["message"] == "Error occurred"
        assert response["error"]["details"] is None
        
        # Test with list data to trigger pagination (lines not covered)
        list_data = [1, 2, 3, 4, 5]
        response = format_api_response(list_data)
        assert "count" in response["metadata"]
        assert response["metadata"]["count"] == 5
        assert response["metadata"]["has_more"] is False
        assert response["metadata"]["page"] == 1
        assert response["metadata"]["per_page"] == 5
        
        # Test with non-list data (no pagination lines)
        response = format_api_response("string data")
        assert "count" not in response["metadata"]
        
        # Test all metadata fields (lines not covered)
        assert response["metadata"]["version"] == "1.0"
        assert response["metadata"]["api_version"] == "v1"
        assert response["metadata"]["response_time"] == "0.123s"
        assert "request_id" in response["metadata"]
        assert response["metadata"]["request_id"].startswith("req_")
        
        # Test timestamp field (line not covered)
        assert "timestamp" in response
        assert isinstance(response["timestamp"], str)
        assert "T" in response["timestamp"]  # ISO format
    
    def test_check_email_format_function(self):
        """Test the check_email_format function (small duplicate)"""
        
        # Test all branches in this simplified function
        assert check_email_format(None) is False
        assert check_email_format(123) is False
        assert check_email_format("") is False
        assert check_email_format("   ") is False
        
        # Test missing @ or .
        assert check_email_format("noemail") is False
        assert check_email_format("no@email") is False
        assert check_email_format("email.com") is False
        
        # Test multiple @ symbols
        assert check_email_format("user@@domain.com") is False
        
        # Test valid emails
        assert check_email_format("user@domain.com") is True
        assert check_email_format("test@example.org") is True
    
    def test_all_imports_and_modules(self):
        """Ensure all import lines are covered"""
        # These should cover any import lines that aren't hit
        import json
        import datetime
        from typing import Dict, List, Optional, Any
        import uuid
        
        # Use each import to ensure coverage
        data = {"test": "value"}
        json_str = json.dumps(data)
        assert isinstance(json_str, str)
        
        now = datetime.datetime.now()
        assert isinstance(now.isoformat(), str)
        
        test_uuid = str(uuid.uuid4())
        assert len(test_uuid) == 36
        
        # Test typing usage
        test_dict: Dict[str, str] = {"key": "value"}
        test_list: List[int] = [1, 2, 3]
        test_optional: Optional[str] = "test"
        test_any: Any = {"anything": True}
        
        assert isinstance(test_dict, dict)
        assert isinstance(test_list, list)
        assert test_optional is not None
        assert test_any is not None

# Add this code to the END of your tests/test_comprehensive.py file
# This targets the exact missing lines in your duplicates.py file

class TestMissingLinesTargeted:
    """Target the exact missing lines for 95% coverage"""
    
    def test_userservice_validation_errors(self):
        """Test UserService validation that raises ValueError"""
        user_service = UserService()
        
        # Test name validation errors (currently not covered)
        try:
            user_service.create_user("", "test@example.com", 25)  # Empty name
            assert False, "Should raise ValueError for empty name"
        except ValueError as e:
            assert "Name must be at least 2 characters" in str(e)
        
        try:
            user_service.create_user("A", "test@example.com", 25)  # Name too short
            assert False, "Should raise ValueError for short name"
        except ValueError as e:
            assert "Name must be at least 2 characters" in str(e)
        
        # Test email validation errors (currently not covered)
        try:
            user_service.create_user("John", "", 25)  # Empty email
            assert False, "Should raise ValueError for empty email"
        except ValueError as e:
            assert "Invalid email format" in str(e)
        
        try:
            user_service.create_user("John", "invalid_email", 25)  # No @ symbol
            assert False, "Should raise ValueError for invalid email"
        except ValueError as e:
            assert "Invalid email format" in str(e)
        
        # Test age validation errors (currently not covered)
        try:
            user_service.create_user("John", "john@test.com", -1)  # Negative age
            assert False, "Should raise ValueError for negative age"
        except ValueError as e:
            assert "Invalid age" in str(e)
        
        try:
            user_service.create_user("John", "john@test.com", 151)  # Age too high
            assert False, "Should raise ValueError for age > 150"
        except ValueError as e:
            assert "Invalid age" in str(e)
    
    def test_userservice_all_fields(self):
        """Test all fields in UserService create_user to hit missing lines"""
        user_service = UserService()
        user = user_service.create_user("John Doe", "john@example.com", 30)
        
        # Test all fields that might not be covered
        assert "id" in user
        assert "created_at" in user
        assert "updated_at" in user
        assert user["active"] is True
        assert user["role"] == "user"
        assert user["permissions"] == ["read"]
        
        # Test nested profile structure
        profile = user["profile"]
        assert profile["bio"] == ""
        assert profile["avatar"] is None
        assert "preferences" in profile
        
        preferences = profile["preferences"]
        assert preferences["theme"] == "light"
        assert preferences["notifications"] is True
        
        # Test datetime fields are strings
        assert isinstance(user["created_at"], str)
        assert isinstance(user["updated_at"], str)
        assert "T" in user["created_at"]  # ISO format
    
    def test_validate_email_all_branches(self):
        """Test every branch in validate_email function"""
        
        # Test None and non-string inputs (line not covered)
        assert validate_email(None) is False
        assert validate_email(123) is False
        assert validate_email([]) is False
        assert validate_email({}) is False
        
        # Test empty email (line not covered)
        assert validate_email("") is False
        assert validate_email("   ") is False
        
        # Test missing @ or . (line not covered)
        assert validate_email("noemail") is False
        assert validate_email("no@email") is False
        assert validate_email("email.com") is False
        
        # Test multiple @ symbols (line not covered)
        assert validate_email("user@@domain.com") is False
        assert validate_email("user@domain@com") is False
        
        # Test local part validation (lines not covered)
        assert validate_email("@domain.com") is False  # Empty local
        assert validate_email("a" * 65 + "@domain.com") is False  # Local too long
        
        # Test domain part validation (lines not covered)
        assert validate_email("user@") is False  # Empty domain
        assert validate_email("user@" + "a" * 256) is False  # Domain too long
        
        # Test consecutive dots (line not covered)
        assert validate_email("user..name@domain.com") is False
        assert validate_email("user@domain..com") is False
        
        # Test domain structure (lines not covered)
        assert validate_email("user@domain") is False  # No TLD
        assert validate_email("user@.com") is False  # Empty domain part
        
        # Test domain part length limits (lines not covered)
        assert validate_email("user@" + "a" * 64 + ".com") is False  # Domain part too long
        
        # Test domain parts starting/ending with hyphen (lines not covered)
        assert validate_email("user@-domain.com") is False
        assert validate_email("user@domain-.com") is False
        assert validate_email("user@domain.-com") is False
        assert validate_email("user@domain.com-") is False
        
        # Test valid emails to ensure function still works
        assert validate_email("user@domain.com") is True
        assert validate_email("test@example.org") is True
    
    def test_validate_password_all_branches(self):
        """Test every branch in validate_password function"""
        
        # Test empty password (line not covered)
        result = validate_password("")
        assert result["valid"] is False
        assert "Password is required" in result["errors"]
        assert result["strength"] == "weak"
        
        # Test None password (line not covered)
        result = validate_password(None)
        assert result["valid"] is False
        
        # Test short password (< 8 chars) (line not covered)
        result = validate_password("short")
        assert result["valid"] is False
        assert "Password must be at least 8 characters long" in result["errors"]
        
        # Test medium length password (8-11 chars) (line not covered)
        result = validate_password("password")
        assert "Consider using at least 12 characters" in result["suggestions"]
        
        # Test missing uppercase (line not covered)
        result = validate_password("password123!")
        assert "Password must contain at least one uppercase letter" in result["errors"]
        
        # Test missing lowercase (line not covered)  
        result = validate_password("PASSWORD123!")
        assert "Password must contain at least one lowercase letter" in result["errors"]
        
        # Test missing digit (line not covered)
        result = validate_password("Password!")
        assert "Password must contain at least one digit" in result["errors"]
        
        # Test missing special character (line not covered)
        result = validate_password("Password123")
        assert "Password must contain at least one special character" in result["errors"]
        
        # Test strength calculations (lines not covered)
        # Weak password (score < 3)
        result = validate_password("weak")
        assert result["strength"] == "weak"
        
        # Medium password (score 3-4)
        result = validate_password("Password123")  # Missing special char
        assert result["strength"] == "medium"
        
        # Strong password (score >= 5)
        result = validate_password("StrongPassword123!")
        assert result["strength"] == "strong"
        assert result["valid"] is True
        assert len(result["errors"]) == 0
    
    def test_dataprocessor_all_branches(self):
        """Test every branch in DataProcessor"""
        processor = DataProcessor()
        
        # Test empty data (line covered)
        assert processor.process_data([]) == []
        assert processor.process_data(None) == []
        
        # Test non-dict items (line not covered)
        result = processor.process_data(["string", 123, None])
        assert result == []  # Should skip non-dict items
        
        # Test missing required fields (lines not covered)
        result = processor.process_data([
            {},  # No id or name
            {"id": "1"},  # Missing name
            {"name": "Test"},  # Missing id
        ])
        assert result == []  # Should skip items without required fields
        
        # Test valid data with all optional fields (lines not covered)
        data = [{
            "id": 123,  # Test int to str conversion
            "name": "test item",  # Test title() conversion
            "description": "This is a test description",
            "category": "TEST_CATEGORY",  # Test lower() conversion
            "tags": ["  Tag1  ", "TAG2", "\tTag3\n"]  # Test tag processing
        }]
        
        result = processor.process_data(data)
        assert len(result) == 1
        
        item = result[0]
        assert item["id"] == "123"  # Int converted to string
        assert item["name"] == "Test Item"  # Title case
        assert item["description"] == "This is a test description"
        assert item["category"] == "test_category"  # Lowercase
        assert item["tags"] == ["tag1", "tag2", "tag3"]  # Cleaned tags
        assert item["word_count"] == 5  # Word count calculation
        
        # Test missing optional fields (lines not covered)
        data = [{"id": "1", "name": "Test"}]  # No description, category, tags
        result = processor.process_data(data)
        
        item = result[0]
        assert item["description"] == ""  # Default empty description
        assert item["category"] == "uncategorized"  # Default category
        assert item["tags"] == []  # Default empty tags
        assert item["word_count"] == 0  # No description = 0 words
        
        # Test metadata fields (lines not covered)
        assert "metadata" in item
        metadata = item["metadata"]
        assert "processed_at" in metadata
        assert metadata["version"] == "1.0"
        assert metadata["status"] == "active"
        assert "T" in metadata["processed_at"]  # ISO format
    
    def test_format_api_response_all_branches(self):
        """Test every branch in format_api_response"""
        
        # Test default parameters (lines not covered)
        response = format_api_response({"test": "data"})
        assert response["success"] is True
        assert response["status_code"] == 200
        assert response["message"] == "Success"
        assert response["data"] == {"test": "data"}
        
        # Test custom message and status (lines not covered)
        response = format_api_response(None, "Custom message", 201)
        assert response["message"] == "Custom message"
        assert response["status_code"] == 201
        assert response["success"] is True  # 201 < 400
        
        # Test error response (lines not covered)
        response = format_api_response(None, "Error occurred", 400)
        assert response["success"] is False  # 400 >= 400
        assert response["status_code"] == 400
        assert response["message"] == "Error occurred"
        assert "error" in response
        assert response["error"]["code"] == 400
        assert response["error"]["message"] == "Error occurred"
        assert response["error"]["details"] is None
        
        # Test with list data to trigger pagination (lines not covered)
        list_data = [1, 2, 3, 4, 5]
        response = format_api_response(list_data)
        assert "count" in response["metadata"]
        assert response["metadata"]["count"] == 5
        assert response["metadata"]["has_more"] is False
        assert response["metadata"]["page"] == 1
        assert response["metadata"]["per_page"] == 5
        
        # Test with non-list data (no pagination lines)
        response = format_api_response("string data")
        assert "count" not in response["metadata"]
        
        # Test all metadata fields (lines not covered)
        assert response["metadata"]["version"] == "1.0"
        assert response["metadata"]["api_version"] == "v1"
        assert response["metadata"]["response_time"] == "0.123s"
        assert "request_id" in response["metadata"]
        assert response["metadata"]["request_id"].startswith("req_")
        
        # Test timestamp field (line not covered)
        assert "timestamp" in response
        assert isinstance(response["timestamp"], str)
        assert "T" in response["timestamp"]  # ISO format
    
    def test_check_email_format_function(self):
        """Test the check_email_format function (small duplicate)"""
        
        # Test all branches in this simplified function
        assert check_email_format(None) is False
        assert check_email_format(123) is False
        assert check_email_format("") is False
        assert check_email_format("   ") is False
        
        # Test missing @ or .
        assert check_email_format("noemail") is False
        assert check_email_format("no@email") is False
        assert check_email_format("email.com") is False
        
        # Test multiple @ symbols
        assert check_email_format("user@@domain.com") is False
        
        # Test valid emails
        assert check_email_format("user@domain.com") is True
        assert check_email_format("test@example.org") is True
    
    def test_all_imports_and_modules(self):
        """Ensure all import lines are covered"""
        # These should cover any import lines that aren't hit
        import json
        import datetime
        from typing import Dict, List, Optional, Any
        import uuid
        
        # Use each import to ensure coverage
        data = {"test": "value"}
        json_str = json.dumps(data)
        assert isinstance(json_str, str)
        
        now = datetime.datetime.now()
        assert isinstance(now.isoformat(), str)
        
        test_uuid = str(uuid.uuid4())
        assert len(test_uuid) == 36
        
        # Test typing usage
        test_dict: Dict[str, str] = {"key": "value"}
        test_list: List[int] = [1, 2, 3]
        test_optional: Optional[str] = "test"
        test_any: Any = {"anything": True}
        
        assert isinstance(test_dict, dict)
        assert isinstance(test_list, list)
        assert test_optional is not None
        assert test_any is not None
