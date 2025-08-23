import requests
import json

BASE_URL = "http://localhost:8000"

def test_auth_endpoints():
    print("🧪 Testing Authentication Endpoints\n")
    
    # Test 1: User Registration
    print("1. Testing User Registration...")
    signup_data = {
        "email": "test@example.com",
        "password": "securepassword123",
        "first_name": "John",
        "last_name": "Doe",
        "company": "Test Company"
    }
    
    response = requests.post(f"{BASE_URL}/auth/signup", json=signup_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        token_data = response.json()
        access_token = token_data["access_token"]
        print(f"✅ Registration successful! Access token: {access_token[:20]}...")
    else:
        print(f"❌ Registration failed: {response.text}")
        return
    
    print("\n" + "="*50 + "\n")
    
    # Test 2: User Login
    print("2. Testing User Login...")
    login_data = {
        "email": "test@example.com",
        "password": "securepassword123"
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        login_token_data = response.json()
        print(f"✅ Login successful! User: {login_token_data['user']['email']}")
    else:
        print(f"❌ Login failed: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 3: Get Current User Info
    print("3. Testing Get Current User Info...")
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ User info retrieved: {user_info['first_name']} {user_info['last_name']}")
    else:
        print(f"❌ Failed to get user info: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 4: Update Profile
    print("4. Testing Profile Update...")
    update_data = {
        "first_name": "John Updated",
        "last_name": "Doe Updated"
    }
    response = requests.put(f"{BASE_URL}/auth/profile", json=update_data, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        updated_user = response.json()
        print(f"✅ Profile updated: {updated_user['first_name']} {updated_user['last_name']}")
    else:
        print(f"❌ Profile update failed: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 5: Forgot Password
    print("5. Testing Forgot Password...")
    forgot_data = {"email": "test@example.com"}
    response = requests.post(f"{BASE_URL}/auth/forgot-password", json=forgot_data)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Forgot password request sent")
    else:
        print(f"❌ Forgot password failed: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 6: Refresh Token
    print("6. Testing Token Refresh...")
    response = requests.post(f"{BASE_URL}/auth/refresh", headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        new_token_data = response.json()
        print(f"✅ Token refreshed: {new_token_data['access_token'][:20]}...")
    else:
        print(f"❌ Token refresh failed: {response.text}")
    
    print("\n" + "="*50 + "\n")
    
    # Test 7: Logout
    print("7. Testing Logout...")
    response = requests.post(f"{BASE_URL}/auth/logout")
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        print("✅ Logout successful")
    else:
        print(f"❌ Logout failed: {response.text}")

if __name__ == "__main__":
    test_auth_endpoints()
