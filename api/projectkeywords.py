import requests
from config import base_url,user_agent
import json
url = f"{base_url}/api/v1/projectkeywords"
headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'environment': 'production',
    'priority': 'u=1, i',
    "User-Agent": user_agent
}

def update_project_keywords(session: requests.Session, token: str, project_name: str, keywords_dict: dict):
    headers['X-CSRF-TOKEN'] = token
    params = {'tzOffset': -18000000}
    data = {
        'projectName': project_name,
        'type': 'incidentlist',
        'keywords': json.dumps(keywords_dict, ensure_ascii=False)
    }

    response = session.post(url, headers=headers, params=params, data=data)

    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')