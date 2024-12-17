from config import *
import requests

def login(session: requests.Session):
    # Step 1: Perform login.py to retrieve token and session ID
    login_url = f"{base_url}/api/v1/login-check"
    login_params = {
        "userName": username,
        "password": password
    }

    login_response = session.post(login_url, params=login_params,
                                  headers={"User-Agent": user_agent, "Content-Type": "application/json"})

    if login_response.status_code != 200:
        print("Login failed:", login_response.text)
        exit(1)

    login_data = login_response.json()
    if not login_data.get("valid", False):
        print("Invalid login.py credentials.")
        exit(1)

    # Extract required csrf_token from the login.py response
    csrf_token = login_data.get("token", "")
    return csrf_token