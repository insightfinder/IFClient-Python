import json

import requests
from config import *

def loadProjectsMetaDataInfo(session: requests.Session, token: str ,projectName):
    projectList = [{"projectName":projectName,"customerName": username}]
    form_data = {"projectList": json.dumps(projectList), "includeInstance": True}

    metadata_response = session.post(f"{base_url}/api/v1/loadProjectsMetaDataInfo",data=form_data, params={'tzOffset': -18000000},
                                     headers={"User-Agent": user_agent, "Content-Type": "application/x-www-form-urlencoded;charset=UTF-8", "X-CSRF-TOKEN": token},)
    response_json = metadata_response.json()
    return response_json


def list_instances_in_project(session: requests.Session, token: str ,projectName):
    result = list()
    project_metadata = loadProjectsMetaDataInfo(session, token,projectName)

    if 'instanceStructureSet' not in project_metadata["data"][0]:
        print("Error to find instanceStructureSet for project ", projectName,project_metadata["data"][0] )
        return result

    instances_dict = project_metadata["data"][0]["instanceStructureSet"]
    for entry in instances_dict:
        result.append(entry['i'])

    return result