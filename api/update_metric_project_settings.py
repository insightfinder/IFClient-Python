import requests
from config import *

def update_metric_project_settings(session: requests.Session,token: str):
    update_settings_url = f"{base_url}/api/v1/watch-tower-setting"
    query_params = {
        "projectName": projectName,
        "customerName": username
    }

    # The session should already contain the cookies returned by the login.py step.
    update_response = session.post(update_settings_url, params=query_params, json=metric_project_settings, headers={"X-CSRF-TOKEN": token,
                                                                                                           "User-Agent": user_agent,
                                                                                                           "Content-Type": "application/json"})
    if update_response.status_code == 200:
        print("Settings updated successfully!")
        print(update_response.text)
    else:
        print("Failed to update settings:", update_response.status_code, update_response.text)