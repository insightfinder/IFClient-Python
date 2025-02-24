import requests
from config import user_agent,metric_project_settings,base_url

def update_metric_project_settings(session: requests.Session,token: str, project_name: str, customer_name:str):
    update_settings_url = f"{base_url}/api/v1/watch-tower-setting"
    query_params = {
        "projectName": project_name,
        "customerName": customer_name
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