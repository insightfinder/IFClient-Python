import requests
from config import user_agent,base_url,username
import json
url =  f"{base_url}/api/v2/systemframework"
headers = {
        'accept': 'application/json, text/plain, */*',
        'environment': 'production',
        'priority': 'u=1, i',
        'user-agent': user_agent
    }

def get_system_framework(session: requests.Session,token: str):
    headers['X-CSRF-TOKEN'] = token
    params = {
        'customerName': username,
        'needDetail': 'false',
        'tzOffset': '-18000000'
    }

    response = session.get(url, headers=headers, params=params)
    response_json = response.json()
    ownSystemArr = response_json['ownSystemArr']
    own_system_dict = {}
    for systemStr in ownSystemArr:
        system_json = json.loads(systemStr)

        # processProjects
        projectListStr = system_json['projectDetailsList']
        projectList = json.loads(projectListStr)
        system_json['projectDetailsList'] = projectList

        own_system_dict[system_json['systemKey']['systemName']] = system_json

    return own_system_dict



def get_projects_in_system(session: requests.Session,token: str, systemID: str, type: str):
    systemFramework = get_system_framework(session,token)
    system_json = systemFramework.get(systemID)
    raw_project_list = system_json['projectDetailsList']
    projectList = []
    for project in raw_project_list:

        # Filter by project type
        if type.lower() == "all":
            projectList.append(project['projectName'])
        elif type.lower() == "log" and project['dataType'].lower() == "log":
            projectList.append(project['projectName'])
        elif type.lower() == "metric" and project['dataType'].lower() == "metric":
            projectList.append(project['projectName'])
        elif type.lower() == "alert" and project['dataType'].lower() == "alert":
            projectList.append(project['projectName'])


    return projectList

def update_system_for_project(session: requests.Session, token: str, project_name:str, system_display_name: str, system_id: str):
    headers['X-CSRF-TOKEN'] = token
    headers['Content-Type'] = 'application/x-www-form-urlencoded;charset=UTF-8'
    params = {
        'tzOffset': '-18000000',
        'ignoreHashVerify': True
    }

    system_info_list = [{"customerName": username, "systemName": system_id,
                      "systemDisplayName": system_display_name,
                      "projectNameSet": [{"projectName": project_name, "userName": username}]}]
    form_data = {
        'customerName': username,
        'operation': 'addProjectToSystem',
        'systemInfo': json.dumps(system_info_list),
    }

    response = session.post(url, headers=headers, params=params, data=form_data)
    print(f'Status Code: {response.status_code}')
    print(f'Response Text: {response.text}')