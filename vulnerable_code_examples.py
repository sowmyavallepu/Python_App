"""
FastAPI Security Demonstration - Intentional Vulnerabilities
FOR DEMO PURPOSES ONLY - Shows security scanner detection
"""

import os
import subprocess
import hashlib
import pickle
import random
import sqlite3

# 1. Hard-coded secrets (Bandit B105, B106)
API_KEY = "sk-1234567890abcdef"
DATABASE_PASSWORD = "admin123"
SECRET_TOKEN = "super_secret_token_12345"
JWT_SECRET = "my-jwt-secret-key"

# 2. SQL Injection vulnerability (Bandit B608)
def unsafe_sql_query(user_input):
    """This creates SQL injection in FastAPI context"""
    query = f"SELECT * FROM users WHERE id = '{user_input}'"
    # Allows: '; DROP TABLE users; --
    return query

# 3. Command injection (Bandit B602, B607)
def unsafe_system_call(user_input):
    """Command injection via API parameter"""
    os.system(f"ping -c 1 {user_input}")  # Command injection
    subprocess.call(f"echo {user_input}", shell=True)  # Shell injection

# 4. Insecure file operations (Bandit B108)
def create_temp_file():
    """Predictable temp file creation"""
    temp_file = "/tmp/api_data.txt"  # Predictable path
    with open(temp_file, 'w') as f:
        f.write("sensitive API data")
    return temp_file

# 5. Unsafe deserialization (Bandit B301)
def unsafe_pickle_load(data):
    """Unsafe pickle in API context"""
    return pickle.loads(data)  # Code execution risk

# 6. Weak cryptography (Bandit B324)
def weak_password_hash(password):
    """Using broken MD5 for passwords"""
    return hashlib.md5(password.encode()).hexdigest()  # MD5 is broken

# 7. Insecure random (Bandit B311)
def generate_api_token():
    """Insecure random for API tokens"""
    return str(random.random())  # Not cryptographically secure

# 8. Try/except pass (Bandit B110)
def api_operation():
    """Silent exception handling in API"""
    try:
        risky_api_call()
    except:
        pass  # Silent fail dangerous for APIs

def risky_api_call():
    raise Exception("API error")

# 9. Assert for validation (Bandit B101)
def validate_api_key(api_key):
    """Using assert for API validation"""
    assert api_key != "admin", "Admin key not allowed"  # Can be disabled
    return True

# 10. Binding to all interfaces (Bandit B104)
API_HOST = "0.0.0.0"  # Security risk
DEBUG_MODE = True     # Should be False in production

# 11. Eval usage (Bandit B307)
def dynamic_api_code(user_code):
    """Dynamic code execution in API"""
    return eval(user_code)  # Arbitrary code execution

# 12. Insecure SSL context
import ssl
def create_insecure_ssl():
    """Insecure SSL for API calls"""
    context = ssl.create_default_context()
    context.check_hostname = False  # Disable hostname check
    context.verify_mode = ssl.CERT_NONE  # Disable cert verification
    return context

# 13. Hardcoded database connection
DATABASE_URL = "postgresql://admin:password123@localhost:5432/mydb"

# 14. Insecure file permissions
def create_api_config():
    """API config with bad permissions"""
    with open("api_config.txt", 'w') as f:
        f.write(f"api_key={API_KEY}\ndatabase_url={DATABASE_URL}")
    os.chmod("api_config.txt", 0o777)  # World writable

# FastAPI-specific vulnerabilities
if __name__ == "__main__":
    print("🚨 FastAPI Security Vulnerability Demonstration")
    print("⚠️  This file contains INTENTIONAL security issues for testing")
    
    print(f"\n1. Hard-coded API Key: {API_KEY[:10]}...")
    print(f"2. Weak MD5 Hash: {weak_password_hash('password')}")
    print(f"3. Insecure API Token: {generate_api_token()}")
    print(f"4. SQL Injection Query: {unsafe_sql_query('1; DROP TABLE users; --')}")
    
    print("\n🔍 Security scanners will detect all these FastAPI security issues!")
