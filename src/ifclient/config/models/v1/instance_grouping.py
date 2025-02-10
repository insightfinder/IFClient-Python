from pydantic import BaseModel, Field
from typing import Dict, Any, List, Literal, Optional

class Instance(BaseModel):
    instanceName: str = Field(
        ...,
        description="The name of the instance.",
        examples=["instance"]
    )
    containerName: Optional[str] = Field(
        default=None,
        description="The name of the container. Required if container project",
        examples=["container"]
    )
    appName: Optional[str] = Field(
        default=None,
        description="Component Name",
        examples=["component"]
    )
    metricInstanceName: Optional[str] = Field(
        default=None,
        description="metricInstanceName. Setting only for log project",
        examples=["metric-instance"]
    )
    ignoreFlag: Optional[bool] = Field(
        default=None,
        description="Ignore all anomalies on the instance",
        examples=[False]
    )
    instanceDisplayName: Optional[str] = Field(
        default=None,
        description="Display name of instance",
        examples=["instance"]
    )


class InstanceGroupingSettingV1(BaseModel):
    apiVersion: Literal["v1"]
    type: Literal["instanceGroupingSetting"]
    instances: Optional[List[Instance]] = Field(
        default=None,
        description="List of instances"
    )
