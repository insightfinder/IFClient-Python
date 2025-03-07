import requests
from api.login import login
from api.systemframework import update_system_for_project
from api.update_metric_project_settings import update_metric_project_settings
from api.projectkeywords import update_project_keywords
from api.systemframework import get_projects_in_system
from config import project_keywords_settings, username
from api.loadProjectsMetaDataInfo import list_instances_in_project
from api.agentUploadInstanceMetadata import batch_update_instance_component_name,batch_update_zone_name
from tabulate import tabulate
from config import component_level_pattern_name_settings
import json
from api.groupingstorage import get_zones_for_instances

def generate_component_name_from_instance_name(instance_name: str) -> str:
    result = instance_name

    if instance_name.lower().find("he-swt") != -1 or instance_name.lower().find("he-sw") != -1:
        result = "HE-SW"

    # 1. Convert all swt to Switch
    elif instance_name.lower().find("swt") != -1 or instance_name.lower().find("sw") != -1 or instance_name.lower().find("switch") != -1:
        result = "Switch"

    # 2.
    elif instance_name.lower().find("enb") != -1:
        result = "eNB"

    elif instance_name.lower().find("isp") != -1:
        result = "ISP"

    elif instance_name.lower().find("mikrotik") != -1 or instance_name.lower().find("microtik") != -1:
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

    elif instance_name.lower().find("smartbox") != -1:
        result = "Smartbox"

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

    # for project_name in get_projects_in_system(session, token, systemID, "alert"):
    #     update_project_keywords(session,token,project_name,project_keywords_settings)

    # all_projects = get_projects_in_system(session, token, systemID, "all")
    # for project in all_projects:
    #     instances = list_instances_in_project(session,token,project)
    #     project_component_instance_mapping = dict()
    #     for instance in instances:
    #         project_component_instance_mapping[instance] = generate_component_name_from_instance_name(instance)

        # table_data = [(key, value) for key, value in project_component_instance_mapping.items()]
        # print(tabulate(table_data, headers=["instanceName", "componentName"], tablefmt="grid"))
        # batch_update_instance_component_name(project,project_component_instance_mapping)



    # metric_projects = get_projects_in_system(session, token, systemID, "metric")
    # for project in metric_projects:
    #     update_metric_project_settings(session, token, project, component_level_pattern_name_settings)




    # project_zone_mapping = dict()
    # metric_projects = get_projects_in_system(session, token, systemID, "metric")
    # for project in metric_projects:
    #     instances = list_instances_in_project(session, token, project)
    #     if len(instances) == 0:
    #         zones = dict()
    #     else:
    #         zones = get_zones_for_instances(session, token, project, instances)
    #
    #     common_project_name = project.replace("-metrics-1","").replace("-metrics","")
    #     project_zone_mapping[common_project_name] = zones
    #
    # alert_projects = get_projects_in_system(session, token, systemID, "alert")
    # for project in alert_projects:
    #     instances = list_instances_in_project(session, token, project)
    #     common_project_name = project.replace("-problems-1","").replace("-problems","")
    #     zones = project_zone_mapping[common_project_name]
    #     if len(zones) != 0:
    #         batch_update_zone_name(project,zones)


    # # Move systems
    # all_projects = get_projects_in_system(session, token, "", "all")
    # for project in all_projects:
    #     update_system_for_project(session, token, project, "", "")





