"""
Secure code examples - all vulnerabilities fixed
"""
import hashlib
import subprocess
import tempfile
import os
from pathlib import Path

# FIXED: Use secure hash instead of MD5
def secure_hash(data):
    """Use SHA-256 instead of MD5"""
    return hashlib.sha256(data.encode()).hexdigest()

# FIXED: Secure subprocess execution
def run_command_safely(command_args):
    """Execute command safely without shell injection"""
    try:
        # Use list of arguments instead of shell=True
        result = subprocess.run(
            command_args,  # Pass as list, not string
            capture_output=True,
            text=True,
            timeout=30,  # Add timeout
            check=True
        )
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Command failed: {e}")
        return None
    except subprocess.TimeoutExpired:
        print("Command timed out")
        return None

# FIXED: Secure file handling
def handle_file_securely(filename):
    """Handle files securely"""
    # Validate filename to prevent path traversal
    safe_filename = os.path.basename(filename)
    
    # Use secure temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        safe_path = Path(temp_dir) / safe_filename
        
        # Ensure file is within temp directory
        try:
            safe_path.resolve().relative_to(Path(temp_dir).resolve())
        except ValueError:
            raise ValueError("Invalid file path")
        
        return str(safe_path)

# FIXED: Secure network binding
def start_secure_server(host='127.0.0.1', port=8000):
    """Bind to localhost only, not all interfaces"""
    # Bind to localhost
