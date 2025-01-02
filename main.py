import re

import json
import requests
import os
from api.instanceMetaData import instanceMetaData
from api.loadProjectsMetaDataInfo import loadProjectsMetaDataInfo
from api.login import login
from api.retrievedatafilter import retrievedatafilter
import pandas as pd
import shutil


def write_csv_file(file_name, content):
    dump_folder = "dump"
    if not os.path.exists(dump_folder):
        os.makedirs(dump_folder)
    dest_file_name = dump_folder + "/" + file_name
    with open(dest_file_name,"w") as file:
        file.write(csv_str)

def delete_dump_files():
    dump_folder = "dump"
    shutil.rmtree(dump_folder)


def process_csv_files():
    # Path to the dump/ folder
    dump_folder = "dump"

    # Iterate over each file in the dump/ folder
    for file_name in os.listdir(dump_folder):
        # Check if the file is a CSV file
        if file_name.endswith(".csv"):
            file_path = os.path.join(dump_folder, file_name)

            # Open the file and process it
            with open(file_path, "r") as file:
                lines = file.readlines()  # Read all lines of the file

            # Check if the file has content
            if lines:
                # Modify the first line (example: adding a prefix "Modified: ")
                split_header = lines[0].split(",")
                for header_index in range(0,len(split_header)):
                    split_header[header_index] = re.sub(r':.*', '', split_header[header_index])
                lines[0] = ",".join(split_header)

            # Save the changes back to the same file
            with open(file_path, "w") as file:
                file.writelines(lines)  # Write the modified lines back

def combine_csv_files(output_file_name):
    # Output file path
    output_file_path = "output/" + output_file_name

    # Path to the dump/ folder
    dump_folder = "dump"

    # List to hold DataFrames of all CSV files
    dataframes = []

    # Track if the 'timestamp' column has already been included
    timestamp_included = False

    # Iterate over each file in the dump/ folder
    for file_name in os.listdir(dump_folder):
        # Check if the file is a CSV file
        if file_name.endswith(".csv"):
            file_path = os.path.join(dump_folder, file_name)

            # Read the CSV file into a DataFrame
            df = pd.read_csv(file_path)

            # If 'timestamp' exists
            if 'timestamp' in df.columns:
                if not timestamp_included:  # Keep the first 'timestamp'
                    timestamp_included = True
                else:  # Drop 'timestamp' from subsequent DataFrames
                    df = df.drop(columns=['timestamp'])

            dataframes.append(df)

    # Concatenate all DataFrames column-wise
    combined_df = pd.concat(dataframes, axis=1)

    # Create the output directory if it doesn't exist
    os.makedirs("output", exist_ok=True)

    # Save the combined DataFrame to the output file
    combined_df.to_csv(output_file_path, index=False)

    print(f"Combined CSV file saved to {output_file_path}")


if __name__ == '__main__':
    session = requests.Session()
    token = login(session)
    # update_metric_project_settings(session,token)

    startTime = 1735707600000
    endTime =   1735848615000

    project_metadata = loadProjectsMetaDataInfo(session, token, startTime, endTime)['data']
    instanceSet = project_metadata[0]['instanceStructureSet']
    instanceIdSet = set()
    for instance in instanceSet:
        instanceIdSet.add(instance['i'])
        for container in instance['c']:
            instanceIdSet.add(container + '_' + instance['i'])

    instance_metadata = instanceMetaData(session, token, instanceIdSet)['data'][0]
    metric_list = set()
    instanceLevelTreeMapNodeInfoMap = json.loads(instance_metadata['result']['instanceLevelTreeMapNodeInfoMap'])
    containerLevelTreeMapNodeInfoMap = json.loads(instance_metadata['result']['containerLevelTreeMapNodeInfoMap'])
    for instance in instanceLevelTreeMapNodeInfoMap:
        instance_info = instanceLevelTreeMapNodeInfoMap[instance]
        for entry in instance_info['metricModelList']:
            metric_list.add(entry['metricName'])

    for container in containerLevelTreeMapNodeInfoMap:
        for container_info in containerLevelTreeMapNodeInfoMap[container]:
            for entry_index in range(0,len(container_info['metricModelList'])):
                entry = container_info['metricModelList'][entry_index]
                metric_list.add(entry['metricName'])

    metric_raw_data_response = retrievedatafilter(session, token, startTime, endTime, instanceIdSet, metric_list)
    raw_csv_data = metric_raw_data_response['splitCsvData']
    for metric_name in raw_csv_data:
        csv_str = raw_csv_data[metric_name]
        write_csv_file(str(startTime) + "_" + str(endTime) + "_" + metric_name + ".csv", csv_str)

    process_csv_files()
    combine_csv_files(str(startTime) + "_" + str(endTime) + ".csv")
    delete_dump_files()

