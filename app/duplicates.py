"""
Minimal duplicate code to demonstrate SonarQube while passing quality gate
Replace your current app/duplicates.py with this content
"""

import json
import datetime
from typing import Dict, List, Optional, Any


# Keep only ONE user management class
class UserService:
    def create_user(self, name: str, email: str, age: int):
        """Create a new user with validation"""
        if not name or len(name) < 2:
            raise ValueError("Name must be at least 2 characters")
        if not email or "@" not in email:
            raise ValueError("Invalid email format")
        if age < 0 or age > 150:
            raise ValueError("Invalid age")
        
        user_data = {
            "id": self.generate_id(),
            "name": name,
            "email": email,
            "age": age,
            "created_at": datetime.datetime.now().isoformat(),
            "updated_at": datetime.datetime.now().isoformat(),
            "active": True,
            "role": "user",
            "permissions": ["read"],
            "profile": {
                "bio": "",
                "avatar": None,
                "preferences": {
                    "theme": "light",
                    "notifications": True
                }
            }
        }
        return user_data

    def generate_id(self):
        import uuid
        return str(uuid.uuid4())


# Keep ONE email validation function
def validate_email(email: str) -> bool:
    """Validate email format with comprehensive checks"""
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    # Basic format check
    if "@" not in email or "." not in email:
        return False
    
    # Split into local and domain parts
    parts = email.split("@")
    if len(parts) != 2:
        return False
    
    local, domain = parts
    
    # Validate local part
    if not local or len(local) > 64:
        return False
    
    # Validate domain part
    if not domain or len(domain) > 255:
        return False
    
    # Check for consecutive dots
    if ".." in email:
        return False
    
    # Check domain has valid structure
    domain_parts = domain.split(".")
    if len(domain_parts) < 2:
        return False
    
    # Validate each domain part
    for part in domain_parts:
        if not part or len(part) > 63:
            return False
        if part.startswith("-") or part.endswith("-"):
            return False
    
    return True


# Keep ONE password validation function
def validate_password(password: str) -> Dict[str, Any]:
    """Validate password strength with detailed feedback"""
    result = {
        "valid": False,
        "strength": "weak",
        "errors": [],
        "suggestions": []
    }
    
    if not password:
        result["errors"].append("Password is required")
        return result
    
    # Length check
    if len(password) < 8:
        result["errors"].append("Password must be at least 8 characters long")
    elif len(password) < 12:
        result["suggestions"].append("Consider using at least 12 characters for better security")
    
    # Character type checks
    has_upper = any(c.isupper() for c in password)
    has_lower = any(c.islower() for c in password)
    has_digit = any(c.isdigit() for c in password)
    has_special = any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password)
    
    if not has_upper:
        result["errors"].append("Password must contain at least one uppercase letter")
    if not has_lower:
        result["errors"].append("Password must contain at least one lowercase letter")
    if not has_digit:
        result["errors"].append("Password must contain at least one digit")
    if not has_special:
        result["errors"].append("Password must contain at least one special character")
    
    # Calculate strength
    strength_score = 0
    if len(password) >= 8:
        strength_score += 1
    if len(password) >= 12:
        strength_score += 1
    if has_upper:
        strength_score += 1
    if has_lower:
        strength_score += 1
    if has_digit:
        strength_score += 1
    if has_special:
        strength_score += 1
    
    if strength_score >= 5:
        result["strength"] = "strong"
    elif strength_score >= 3:
        result["strength"] = "medium"
    else:
        result["strength"] = "weak"
    
    result["valid"] = len(result["errors"]) == 0
    return result


# Keep ONE data processing class
class DataProcessor:
    def process_data(self, data: List[Dict]):
        """Process raw data and return formatted results"""
        if not data:
            return []
        
        processed_results = []
        for item in data:
            if not isinstance(item, dict):
                continue
            
            # Validate required fields
            if "id" not in item or "name" not in item:
                continue
            
            # Clean and format data
            cleaned_item = {
                "id": str(item["id"]).strip(),
                "name": str(item["name"]).strip().title(),
                "description": item.get("description", "").strip(),
                "category": item.get("category", "uncategorized").lower(),
                "tags": [tag.strip().lower() for tag in item.get("tags", [])],
                "metadata": {
                    "processed_at": datetime.datetime.now().isoformat(),
                    "version": "1.0",
                    "status": "active"
                }
            }
            
            # Additional processing
            if cleaned_item["description"]:
                cleaned_item["word_count"] = len(cleaned_item["description"].split())
            else:
                cleaned_item["word_count"] = 0
            
            processed_results.append(cleaned_item)
        
        return processed_results


# Keep ONE API response function
def format_api_response(data: Any, message: str = "Success", status_code: int = 200) -> Dict:
    """Format API response with consistent structure"""
    response = {
        "success": status_code < 400,
        "status_code": status_code,
        "message": message,
        "timestamp": datetime.datetime.now().isoformat(),
        "data": data,
        "metadata": {
            "version": "1.0",
            "api_version": "v1",
            "response_time": "0.123s",
            "request_id": f"req_{datetime.datetime.now().timestamp()}"
        }
    }
    
    # Add pagination info if data is a list
    if isinstance(data, list):
        response["metadata"]["count"] = len(data)
        response["metadata"]["has_more"] = False
        response["metadata"]["page"] = 1
        response["metadata"]["per_page"] = len(data)
    
    # Add error details for non-success responses
    if status_code >= 400:
        response["error"] = {
            "code": status_code,
            "message": message,
            "details": None
        }
    
    return response


# Add just ONE small duplicate to still demonstrate detection (5-10% duplication)
def check_email_format(email: str) -> bool:
    """Alternative email validation - slight duplicate for demo"""
    if not email or not isinstance(email, str):
        return False
    
    email = email.strip().lower()
    
    if "@" not in email or "." not in email:
        return False
    
    parts = email.split("@")
    if len(parts) != 2:
        return False
    
    return True  # Simplified version
