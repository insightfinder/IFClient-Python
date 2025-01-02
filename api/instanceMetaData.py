import json

import requests
from config import *
from urllib.parse import urlencode

def instanceMetaData(session: requests.Session, token: str, instance_list: list[str]):
    headers = {"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
               "X-CSRF-TOKEN": token}
    data = {
        'idList': json.dumps(instance_list),
        'projectName': projectName,
        'instanceGroup': 'All'
    }

    # Define URL and parameters
    url = f"{base_url}/api/v1/instanceMetaData"

    # Send POST request
    response = session.post(url, headers=headers, params={'tzOffset': -18000000}, data=data)

    # Return response
    return response.json()

