import json

import requests
from config import base_url,user_agent

def create_causal_group(session: requests.Session, token: str ,projects: list[str], zoneName: str, userName: str):
    projectNameArr = []
    projectLevelSetting = []
    for project in projects:
        projectNameArr.append(project+"@"+userName)
        duration = 5 * 60 * 1000 if "problems" in project else 45 * 60 * 1000
        projectLevelSettingData = {
            "projectName":project,
            "durationThreshold":duration,
            "considerAnomalyAfterIncident":False,
            "logValidPairDuration":43200000
        }
        projectLevelSetting.append(projectLevelSettingData)
    data = {
        "causalName": zoneName,
        "intervalInDay": 7,
        "retentionTime": 2678400000,
        "enableInterRelation": True,
        "enableComponentIntra": False,
        "enableIncidentOnly": False,
        "includeTargetAnomalyInPossibility": False,
        "projectNameArr": json.dumps(projectNameArr),
        "grouping": json.dumps(["All","All"]),
        "projectLevelSetting": json.dumps(projectLevelSetting),
        "eventsRelationLookBackWindow": 0,
        "owner": userName,
        "validateProjectList": [],
        "concurrencyToleranceWindow": 0,
        "enableSameZone": True
    }
    response = session.post(f"{base_url}/api/v1/causalgroup", params={'tzOffset': -18000000},
                                     headers={"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "X-CSRF-TOKEN": token},data=data)
    response_json = response.json()
    print(response_json)
    return response_json