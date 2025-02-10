from pydantic import BaseModel, AnyUrl, Field
from typing import Literal
from ifclient.config.models.common.file_reference import FileReference

class ToolConfigV1(BaseModel):
    apiVersion: Literal["v1"]
    type: Literal["toolConfig"]
    baseUrl: AnyUrl = Field(
        help="InsightFinder URL where projects are hosted"
    )
    projectBaseConfigs: FileReference # List of file paths or glob patterns
