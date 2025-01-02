import sqlite3

import json
import requests

from api.instanceMetaData import instanceMetaData
from api.loadProjectsMetaDataInfo import loadProjectsMetaDataInfo
from api.login import login
from api.retrievedatafilter import retrievedatafilter

if __name__ == '__main__':
    session = requests.Session()
    token = login(session)
    # update_metric_project_settings(session,token)

    startTime = 1735171200000
    endTime = 1735257599999

    project_metadata = loadProjectsMetaDataInfo(session, token, startTime, endTime)['data'][0]
    instanceSet = project_metadata['instanceStructureSet']
    instanceIdList = []
    for instance in instanceSet:
        instanceIdList.append(instance['i'])

    instance_metadata = instanceMetaData(session, token, instanceIdList)['data'][0]
    metric_list = []
    instanceLevelTreeMapNodeInfoMap = json.loads(instance_metadata['result']['instanceLevelTreeMapNodeInfoMap'])
    for instance in instanceLevelTreeMapNodeInfoMap:
        instance_info = instanceLevelTreeMapNodeInfoMap[instance]
        for entry in instance_info['metricModelList']:
            metric_list.append(entry['metricName'])

    metric_raw_data_response = retrievedatafilter(session, token, startTime, endTime, instanceIdList, metric_list)
    raw_csv_data = metric_raw_data_response['splitCsvData']
    print(raw_csv_data)
