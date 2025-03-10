import json

import requests
from config import base_url,user_agent

def get_grouping_storage_for_instances(session: requests.Session, token: str ,project: str,instances: list[str]):
    data = {
        'projectName': project,
        'instanceGroup': 'All',
        'instanceList': json.dumps(instances)
    }
    response = session.post(f"{base_url}/api/v1/groupingstorage", params={'tzOffset': -18000000},
                                     headers={"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "X-CSRF-TOKEN": token},data=data)
    response_json = response.json()
    return response_json


def get_zones_for_instances(session: requests.Session, token: str ,project: str,instances: list[str]):
    grouping_storage = get_grouping_storage_for_instances(session, token,project,instances)
    zones = grouping_storage["zoneData"]
    return zones