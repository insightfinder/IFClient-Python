import json

import requests
from config import *
from urllib.parse import urlencode

def retrievedatafilter(session: requests.Session, token: str, startTime, endTime, instance_list, metric_list, ):
    headers = {"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8",
               "X-CSRF-TOKEN": token}
    data = {
        'projectName': projectName + '@' + projectOwner,
        'grouping': 'All',
        "startTimestamp": startTime,
        "endTimestamp": endTime,
        "instanceList": json.dumps(list(instance_list)),
        "metricList": json.dumps(list(metric_list)),
        "predictedFlag": True
    }

    # Define URL and parameters
    url = f"{base_url}/api/v1/retrievedatafilter"

    # Send POST request
    response = session.post(url, headers=headers, params={'tzOffset': -18000000}, data=data)

    # Return response
    return response.json()

