import requests
from config import base_url,user_agent
import json
from config import username,license_key

headers = {
    'accept': 'application/json',
    'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
    'environment': 'production',
    'priority': 'u=1, i',
    "User-Agent": user_agent
}

'''
project_name: The project name
instance_component_name_dict: {"instance1": "component1", "instance2": "component2"}
'''
def batch_update_instance_component_name(project_name: str, instance_component_name_dict: dict):
    url = f"{base_url}/api/v1/agent-upload-instancemetadata?userName={username}&licenseKey={license_key}&projectName={project_name}&override=true"

    # Build request body
    json_body = []
    for instance, component in instance_component_name_dict.items():
        json_body.append({
            "instanceName": instance,
            "componentName": component
        })

    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=json.dumps(json_body))
    print(f'Successfully updated the component names for project {project_name} with statue code: {response.status_code}')