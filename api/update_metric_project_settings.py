import requests
from config import user_agent,base_url,username

def update_metric_project_settings(session: requests.Session,token: str, project_name: str, settings: dict):
    update_settings_url = f"{base_url}/api/v1/watch-tower-setting"
    query_params = {
        "projectName": project_name,
        "customerName": username
    }

    # The session should already contain the cookies returned by the login.py step.
    update_response = session.post(update_settings_url, params=query_params, json=settings, headers={"X-CSRF-TOKEN": token,
                                                                                                           "User-Agent": user_agent,
                                                                                                           "Content-Type": "application/json"})
    if update_response.status_code == 200:
        print(f"Settings updated successfully for project {project_name}")
        print(update_response.text)
    else:
        print(f"Failed to update settings for project {project_name}", update_response.status_code, update_response.text)