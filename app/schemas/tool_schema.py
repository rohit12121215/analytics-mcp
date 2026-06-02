from pydantic import BaseModel
from typing import Dict, Any


class ToolRequest(BaseModel):
    tool_name: str
    payload: Dict[str, Any]