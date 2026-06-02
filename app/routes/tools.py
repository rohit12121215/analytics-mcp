from fastapi import APIRouter

from app.schemas.tool_schema import ToolRequest
from app.tools.router import execute_tool

router = APIRouter(
    prefix="/tools",
    tags=["Tools"]
)


@router.post("/execute")
async def run_tool(request: ToolRequest):

    result = await execute_tool(
        request.tool_name,
        request.payload
    )

    return result