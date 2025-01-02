import json

import requests
from config import *

def loadProjectsMetaDataInfo(session: requests.Session, token: str , startTime: int, endTime: int):
    projectList = [{"projectName":projectName,"customerName": projectOwner}]
    form_data = {"projectList": json.dumps(projectList), "startTime": startTime, "endTime": endTime, "includeInstance": True}

    metadata_response = session.post(f"{base_url}/api/v1/loadProjectsMetaDataInfo",data=form_data, params={'tzOffset': -18000000},
                                     headers={"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "X-CSRF-TOKEN": token},)
    return metadata_response.json()


