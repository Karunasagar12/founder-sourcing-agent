import requests
import json

# Test configuration
BASE_URL = "http://localhost:8000"
AUTH_URL = f"{BASE_URL}/auth"

def test_auth_endpoints():
    """Test all authentication endpoints"""
    
    print("🧪 Testing Authentication Endpoints")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1. Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"❌ Health check failed: {e}")
    
    # Test 2: Signup
    print("\n2. Testing signup endpoint...")
    signup_data = {
        "email": "test@example.com",
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Company",
        "password": "SecurePass123!"
    }
    
    try:
        response = requests.post(f"{AUTH_URL}/signup", json=signup_data)
        print(f"✅ Signup: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   User created: {result['user']['email']}")
            print(f"   Token received: {result['access_token'][:20]}...")
            token = result['access_token']
        else:
            print(f"   Error: {response.text}")
            token = None
    except Exception as e:
        print(f"❌ Signup failed: {e}")
        token = None
    
    # Test 3: Login
    print("\n3. Testing login endpoint...")
    login_data = {
        "email": "test@example.com",
        "password": "SecurePass123!"
    }
    
    try:
        response = requests.post(f"{AUTH_URL}/login", json=login_data)
        print(f"✅ Login: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   User logged in: {result['user']['email']}")
            print(f"   Token received: {result['access_token'][:20]}...")
            token = result['access_token']
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Login failed: {e}")
    
    # Test 4: Get current user (with token)
    if token:
        print("\n4. Testing get current user endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        
        try:
            response = requests.get(f"{AUTH_URL}/me", headers=headers)
            print(f"✅ Get current user: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   User: {result['email']}")
                print(f"   Name: {result['first_name']} {result['last_name']}")
                print(f"   Company: {result['company']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Get current user failed: {e}")
    
    # Test 5: Update profile
    if token:
        print("\n5. Testing update profile endpoint...")
        headers = {"Authorization": f"Bearer {token}"}
        update_data = {
            "first_name": "John Updated",
            "company": "Updated Company"
        }
        
        try:
            response = requests.put(f"{AUTH_URL}/profile", json=update_data, headers=headers)
            print(f"✅ Update profile: {response.status_code}")
            if response.status_code == 200:
                result = response.json()
                print(f"   Updated name: {result['first_name']}")
                print(f"   Updated company: {result['company']}")
            else:
                print(f"   Error: {response.text}")
        except Exception as e:
            print(f"❌ Update profile failed: {e}")
    
    # Test 6: Forgot password
    print("\n6. Testing forgot password endpoint...")
    forgot_data = {"email": "test@example.com"}
    
    try:
        response = requests.post(f"{AUTH_URL}/forgot-password", json=forgot_data)
        print(f"✅ Forgot password: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print(f"   Message: {result['message']}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"❌ Forgot password failed: {e}")
    
    print("\n" + "=" * 50)
    print("🎉 Authentication system test completed!")

if __name__ == "__main__":
    test_auth_endpoints()
