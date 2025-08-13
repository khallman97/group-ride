#!/usr/bin/env python3
"""
Simple CORS test script
"""
import requests

def test_cors():
    """Test CORS configuration"""
    base_url = "http://localhost:8000"
    
    print("Testing CORS configuration...")
    
    # Test 1: Simple GET request
    print("\n1. Testing GET request to /debug/cors")
    try:
        response = requests.get(f"{base_url}/debug/cors")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 2: OPTIONS preflight request
    print("\n2. Testing OPTIONS preflight request")
    try:
        response = requests.options(f"{base_url}/debug/cors")
        print(f"Status: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
    except Exception as e:
        print(f"Error: {e}")
    
    # Test 3: Test with Origin header (simulating browser request)
    print("\n3. Testing with Origin header")
    try:
        headers = {
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
            "Access-Control-Request-Headers": "Content-Type,Authorization"
        }
        response = requests.options(f"{base_url}/auth/signup", headers=headers)
        print(f"Status: {response.status_code}")
        print(f"CORS Headers:")
        for header, value in response.headers.items():
            if 'access-control' in header.lower():
                print(f"  {header}: {value}")
    except Exception as e:
        print(f"Error: {e}")
    
    print("\nCORS test completed!")

if __name__ == "__main__":
    test_cors()
