import yaml
from pathlib import Path
from typing import Any, Dict
import glob
import itertools
import os
from ifclient.config.models.common.file_reference import FileReference
from ifclient.exceptions.config import EmptyYAMLError

def load_yaml(file_path: str) -> Dict[str, Any]:

    with open(file_path, 'r') as f:
        content = f.read()
    try:
        data = yaml.safe_load(content)
    except yaml.YAMLError as e:
        raise e
    else:
        if data is None:
            raise EmptyYAMLError(f"File {file_path} is an empty yaml file")
        else:
            return data


def validate_config_file(file_path: str) -> Any:
    """
    Load and validate a configuration file by dispatching to the correct model.
    """
        
    data = load_yaml(file_path)

    api_version = data.get("apiVersion", "v1")  # Default to v1 if unspecified
    config_type = data.get("type")
    
    if api_version == "v1":
        if config_type == "toolConfig":
            from ifclient.config.models.v1.tool_config import ToolConfigV1
            return ToolConfigV1(**data)
        elif config_type == "projectBase":
            from ifclient.config.models.v1.project_base import ProjectBaseV1
            return ProjectBaseV1(**data)
        elif config_type == "instanceGroupingSetting":
            from ifclient.config.models.v1.instance_grouping import InstanceGroupingSettingV1
            return InstanceGroupingSettingV1(**data)
        elif config_type == "consumerMetricSetting":
            from ifclient.config.models.v1.consumer_metric import ConsumerMetricSettingV1
            return ConsumerMetricSettingV1(**data)
        else:
            raise ValueError(f"Unknown configuration type for v1: {config_type}")
    else:
        raise ValueError(f"Unsupported apiVersion: {api_version}")

def validate_and_resolve(file_path: str, skip_empty_files: bool) -> Any:
    """
    Validate a configuration file and, if it contains file references,
    load and validate those as well.
    """
    try:
        print(f"Validating file {file_path}")
        validated = validate_config_file(file_path)
    except EmptyYAMLError as e:
        if skip_empty_files:
            print(f"Skipping file {file_path} as it is empty and --skip-empty-files flag is set")
            return None
        else:
            raise Exception(f"{file_path} is empty. Please provide a non-empty YAML file or set --skip-empty-files flag to True to skip empty files")
    except Exception as e:
        raise Exception(f"Error validating file {file_path}: {e}")
    else:
        print(f"File {file_path} is valid")
        # print(f"{validated}")
        validated_file_references = { name: value for name, value in validated.__dict__.items() if isinstance(value, FileReference) }
        for name, value in validated_file_references.items():
            parent_dir = os.path.dirname(file_path)
            resolved_paths = [ glob.glob(path if os.path.isabs(path) else os.path.abspath(os.path.join(parent_dir, path))) for path in value.files ]
            resolved_paths_flattened = list(set(itertools.chain(*resolved_paths)))
            # print(f"Resolved paths for {file_path}: {resolved_paths}")
            setattr(getattr(validated, name), 'files', resolved_paths_flattened)
            for file in resolved_paths_flattened:
                validate_and_resolve(file, skip_empty_files)
        return validated
