from app.tools.registry import TOOLS


async def execute_tool(tool_name: str, payload: dict):

    try:

        # Validate tool exists
        if tool_name not in TOOLS:

            return {
                "success": False,
                "error": f"Tool '{tool_name}' not found"
            }

        # Load tool function
        tool_function = TOOLS[tool_name]

        # Execute tool
        result = await tool_function(payload)

        return {
            "success": True,
            "data": result
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }