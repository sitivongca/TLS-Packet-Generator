import os
import ctypes


# Workaround to load compiled OpenSSL DLLs

def load_openssl():
    """Load OpenSSL DLLs relative to the project structure"""
    # Get the project root directory
    project_dir = os.getcwd()
    
    # Path to OpenSSL DLLs
    openssl_path = os.path.join(project_dir, '.venv', 'openssl', 'bin')
    
    try:
        ctypes.cdll.LoadLibrary(os.path.join(openssl_path, "libcrypto-3-x64.dll"))
        ctypes.cdll.LoadLibrary(os.path.join(openssl_path, "libssl-3-x64.dll"))
        return True
    except Exception as e:
        print(f"Error loading OpenSSL: {e}")
        return False

# Optionally load immediately when imported
#openssl_loaded = load_openssl()
