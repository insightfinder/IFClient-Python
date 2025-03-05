import requests
from api.login import login
from api.update_metric_project_settings import update_metric_project_settings
from api.projectkeywords import update_project_keywords
from api.systemframework import get_projects_in_system
from config import project_keywords_settings, username,systemID
from api.loadProjectsMetaDataInfo import list_instances_in_project
from api.agentUploadInstanceMetadata import batch_update_instance_component_name
from tabulate import tabulate

def generate_component_name_from_instance_name(instance_name: str) -> str:
    result = instance_name

    # 1. Convert all swt to Switch
    if instance_name.lower().find("swt") != -1 or instance_name.lower().find("sw") != -1 or instance_name.lower().find("switch") != -1:
        result = "Switch"

    # 2.
    elif instance_name.lower().find("enb") != -1:
        result = "eNB"

    elif instance_name.lower().find("isp") != -1:
        result = "ISP"

    elif instance_name.lower().find("mikrotik") != -1:
        result = "Mikrotik"

    elif instance_name.lower().find("esxi") != -1:
        result = "ESXi"

    elif instance_name.lower().find("pdu") != -1:
        result = "PDU"

    elif instance_name.lower().find("ups") != -1:
        result = "UPS"

    elif instance_name.lower().find("cpe") != -1:
        result = "CPE"

    elif instance_name.lower().find("ap") != -1:
        result = "AP"

    elif instance_name.lower().find("wan") != -1:
        result = "WAN"

    elif instance_name.lower().find("router") != -1:
        result = "Router"

    elif instance_name.lower().find("ptp") != -1:
        result = "PTP"

    elif instance_name.lower().find("olt") != -1:
        result = "OLT"


    if result == instance_name:
        print("Unable to generate component name for instance: {}".format(instance_name))

    return result

if __name__ == '__main__':
    session = requests.Session()
    token = login(session)

    # for project_name in get_projects_in_system(session,token,systemID,"metric"):
    #     update_metric_project_settings(session, token, project_name, username)
    # for project_name in get_projects_in_system(session, token, systemID, "alert"):
    #     update_project_keywords(session,token,project_name,project_keywords_settings)

    metric_projects = get_projects_in_system(session, token, systemID, "metric")
    for project in metric_projects:
        instances = list_instances_in_project(session,token,project)
        project_component_instance_mapping = dict()
        for instance in instances:
            project_component_instance_mapping[instance] = generate_component_name_from_instance_name(instance)
        table_data = [(key, value) for key, value in project_component_instance_mapping.items()]
        print(tabulate(table_data, headers=["instanceName", "componentName"], tablefmt="grid"))
        input("Press Enter to confirm...")
        batch_update_instance_component_name(project,project_component_instance_mapping)









