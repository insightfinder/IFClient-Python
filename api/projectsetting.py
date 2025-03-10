import json

import requests
from config import base_url,user_agent,username

def get_project_settings(session: requests.Session, token: str ,project: str):
    response = session.get(f"{base_url}/api/v2/project-setting", params={'tzOffset': -18000000, 'projectList': json.dumps([{"projectName":project,"customerName":username}])},
                                     headers={"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "X-CSRF-TOKEN": token})
    response_json = response.json()
    settingsStr = response_json['settingList'][project]
    settingsJson = json.loads(settingsStr)
    return settingsJson['DATA']


def update_project_settings(session: requests.Session, token: str ,project: str,settings: dict):
    data = {
        'projectList': [{"projectName":project,"customerName":username}],
        'setting': settings,
        'touchedSensitivitySetting': True,
        'dataType': "Log"
    }

    response = session.put(f"{base_url}/api/v2/project-setting", params={'tzOffset': -18000000,},
                           headers={"User-Agent": user_agent,
                                    "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
                                    "X-CSRF-TOKEN": token})
    response_json = response.json()
    return response_json